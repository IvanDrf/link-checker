package checker

import (
	"context"
	"net/http"
	"strings"
	"time"
)

type LinkChecker interface {
	CheckLink(ctx context.Context, url string) bool
}

type linkChecker struct {
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

func NewLinkChecker() LinkChecker {
	return &linkChecker{
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

func (u *linkChecker) CheckLink(ctx context.Context, link string) bool {
	if !strings.HasPrefix(link, "https://") && !strings.HasPrefix(link, "http://") {
		link = "https://" + link
	}

	request, err := http.NewRequestWithContext(ctx, http.MethodHead, link, nil)
	if err != nil {
		return false
	}

	resp, err := u.client.Do(request)
	if err != nil {
		return false
	}
	defer resp.Body.Close()

	return resp.StatusCode >= http.StatusOK && resp.StatusCode < http.StatusBadRequest
}
