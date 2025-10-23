package checker

import (
	"context"
	"net/http"
	"strings"
	"time"
)

type UrlChecker interface {
	CheckUrl(ctx context.Context, url string) bool
}

type urlChecker struct {
	client http.Client
}

const (
	requestTimeOut = 3 * time.Second

	maxKeepAliveConns        = 100
	maxKeepAliveCoonsForHost = 20

	maxKeepAliveTime      = 10 * time.Second
	maxTLSHandshakeTime   = 2 * time.Second
	maxResponseHeaderTime = 2 * time.Second
)

func NewUrlChecker() UrlChecker {
	return &urlChecker{
		client: http.Client{
			Timeout: requestTimeOut,
			Transport: &http.Transport{
				MaxIdleConns:          maxKeepAliveConns,
				MaxIdleConnsPerHost:   maxKeepAliveCoonsForHost,
				IdleConnTimeout:       maxKeepAliveTime,
				TLSHandshakeTimeout:   maxTLSHandshakeTime,
				ResponseHeaderTimeout: maxResponseHeaderTime,
			},
		},
	}
}

func (u *urlChecker) CheckUrl(ctx context.Context, url string) bool {
	if !strings.HasPrefix(url, "https://") {
		url = "https://" + url
	}

	request, err := http.NewRequestWithContext(ctx, http.MethodHead, url, nil)
	if err != nil {
		return false
	}

	resp, err := u.client.Do(request)
	if err != nil {
		return false
	}
	defer resp.Body.Close()

	return resp.StatusCode >= 200 && resp.StatusCode < 400
}
