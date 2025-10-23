package urlService

import (
	workerPool "checker/checker/internal/infrastructure"
	"checker/checker/internal/models"
	"checker/checker/pkg/checker"
	"context"
)

type UrlChecker interface {
	CheckUrls(ctx context.Context, links []string) []models.Url
}

type urlChecker struct {
	urlsChecker checker.UrlChecker
}

func NewUrlChecker() UrlChecker {
	return &urlChecker{
		urlsChecker: checker.NewUrlChecker(),
	}
}

func (u *urlChecker) CheckUrls(ctx context.Context, links []string) []models.Url {
	in := make(chan string)
	go fillUrls(in, links)

	out := make(chan models.Url)
	go workerPool.WorkerPool(ctx, in, out, u.urlsChecker.CheckUrl)

	res := []models.Url{}
	for val := range out {
		res = append(res, val)
	}

	return res
}

func fillUrls(in chan string, links []string) {
	defer close(in)
	for i := range links {
		in <- links[i]
	}
}
