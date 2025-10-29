package linkService

import (
	"context"
	"fmt"
	"log/slog"
	"time"

	workerPool "github.com/IvanDrf/checker/internal/infrastructure/workerPool"
	"github.com/IvanDrf/checker/internal/models"
	"github.com/IvanDrf/checker/internal/repo"
	redisCache "github.com/IvanDrf/checker/internal/repo/redis"
	"github.com/IvanDrf/checker/internal/service"
	"github.com/IvanDrf/checker/pkg/checker"

	"github.com/redis/go-redis/v9"
)

type linkChecker struct {
	cacheRepo   repo.CacheRepo
	linkChecker checker.LinkChecker

	logger *slog.Logger
}

func NewLinkChecker(db *redis.Client, logger *slog.Logger) service.LinkChecker {
	return &linkChecker{
		cacheRepo:   redisCache.NewCacheRepo(db),
		linkChecker: checker.NewLinkChecker(),

		logger: logger,
	}
}

func (l *linkChecker) CheckLinks(ctx context.Context, links []string) []models.Link {
	in := make(chan string, len(links))
	out := make(chan models.Link, len(links))

	go l.sendLinks(ctx, in, out, links)
	go workerPool.WorkerPool(ctx, in, out, len(links), l.linkChecker.CheckLink)

	res := make([]models.Link, 0, len(links))
	for link := range out {
		l.logger.Debug(fmt.Sprintf("CheckLinks -> done: %s", link.Link))

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

			l.logger.Debug(fmt.Sprintf("sendLinks-> %s", err.Error()))
		} else {
			l.logger.Debug(fmt.Sprintf("sendLinks -> link: %s", links[i]))
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
	l.logger.Debug(fmt.Sprintf("saveLinks -> start saving links: %v", len(links)))
	l.logger.Info(fmt.Sprintf("links to reddis: %v", len(links)))
	ctx, cancel := context.WithTimeout(context.Background(), linksSavingTime)
	defer cancel()

	redisLinks := make([]interface{}, 0, len(links))
	for i := range len(links) {
		redisLinks = append(redisLinks, links[i].Link, links[i].Status)
	}

	l.cacheRepo.SaveLinks(ctx, &redisLinks)

	l.logger.Debug(fmt.Sprintf("saveLinks -> done saving links: %v", len(links)))
}
