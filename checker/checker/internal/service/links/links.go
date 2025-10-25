package linkService

import (
	workerPool "checker/checker/internal/infrastructure"
	"checker/checker/internal/models"
	"checker/checker/internal/repo"
	redisCache "checker/checker/internal/repo/redis"
	"checker/checker/internal/service"
	"checker/checker/pkg/checker"
	"context"
	"fmt"
	"log/slog"
	"time"

	"github.com/redis/go-redis/v9"
)

type linkChecker struct {
	cacheRepo   repo.CacheRepo
	linkChecker checker.LinkChecker

	log *slog.Logger
}

func NewLinkChecker(db *redis.Client, logger *slog.Logger) service.LinkChecker {
	return &linkChecker{
		cacheRepo:   redisCache.NewCacheRepo(db),
		linkChecker: checker.NewLinkChecker(),

		log: logger,
	}
}

func (l *linkChecker) CheckLinks(ctx context.Context, links []string) []models.Link {
	in := make(chan string, len(links))
	out := make(chan models.Link, len(links))

	go l.sendLinks(ctx, in, out, links)
	go workerPool.WorkerPool(ctx, in, out, len(links), l.linkChecker.CheckLink)

	res := make([]models.Link, 0, len(links))
	for link := range out {
		l.log.Debug(fmt.Sprintf("CheckLinks -> done: %s", link.Link))

		res = append(res, link)
	}

	go l.saveLinks(res)

	return res
}

func (l *linkChecker) sendLinks(ctx context.Context, in chan string, out chan models.Link, links []string) {
	defer close(in)

	for i := range links {
		linkStatus, err := l.cacheRepo.GetLink(ctx, links[i])
		if err != nil {
			in <- links[i]

			l.log.Debug(fmt.Sprintf("sendLinks-> %s", err.Error()))
		} else {
			l.log.Debug(fmt.Sprintf("sendLinks -> link: %s", links[i]))
			out <- models.Link{
				Link:    links[i],
				Status:  linkStatus,
				Checked: false,
			}
		}
	}
}

const linksSavingTime = 2 * time.Second

func (l *linkChecker) saveLinks(links []models.Link) {
	l.log.Debug(fmt.Sprintf("saveLinks -> start saving links: %v", len(links)))
	l.log.Info(fmt.Sprintf("links to reddis: %v", len(links)))
	ctx, cancel := context.WithTimeout(context.Background(), linksSavingTime)
	defer cancel()

	redisLinks := make([]interface{}, 0, len(links))
	for i := range len(links) {
		redisLinks = append(redisLinks, links[i].Link, links[i].Status)
	}

	l.cacheRepo.SaveLinks(ctx, &redisLinks)

	l.log.Debug(fmt.Sprintf("saveLinks -> done saving links: %v", len(links)))
}
