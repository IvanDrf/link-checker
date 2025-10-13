package checker

import (
	"context"
	"net/http"
	"strings"
)

type UrlChecker interface {
	CheckUrl(ctx context.Context, url string) bool
}

type urlChecker struct {
	client http.Client
}

func NewUrlChecker() UrlChecker {
	return &urlChecker{
		client: http.Client{},
	}
}

func (u *urlChecker) CheckUrl(ctx context.Context, url string) bool {
	if !strings.HasPrefix(url, "https://") {
		url = "https://" + url
	}

	request, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return false
	}

	_, err = u.client.Do(request)

	return err == nil
}
