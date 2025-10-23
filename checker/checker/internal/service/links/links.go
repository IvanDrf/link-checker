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
	urlsChecker checker.UrlChecker

	log *slog.Logger
}

func NewLinkChecker(db *redis.Client, logger *slog.Logger) service.LinkChecker {
	return &linkChecker{
		cacheRepo:   redisCache.NewCacheRepo(db),
		urlsChecker: checker.NewUrlChecker(),

		log: logger,
	}
}

func (l *linkChecker) CheckLinks(ctx context.Context, links []string) []models.Link {
	in := make(chan string, len(links))
	out := make(chan models.Link, len(links))

	go l.sendLinks(ctx, in, out, links)
	go workerPool.WorkerPool(ctx, in, out, len(links), l.urlsChecker.CheckUrl)

	res := []models.Link{}
	for link := range out {
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
			out <- models.Link{
				Link:    links[i],
				Status:  linkStatus,
				Checked: false,
			}
		}
	}
}

const linkSavingTime = 2 * time.Second

func (l *linkChecker) saveLinks(links []models.Link) {
	ctx, cancel := context.WithTimeout(context.Background(), linkSavingTime)
	defer cancel()

	for _, link := range links {
		l.saveLink(ctx, &link)
	}
}

func (l *linkChecker) saveLink(ctx context.Context, link *models.Link) {
	err := l.cacheRepo.SaveLink(ctx, link)
	if err != nil {
		l.log.Warn(fmt.Sprintf("saveLink -> %s", err.Error()))
	}
}
