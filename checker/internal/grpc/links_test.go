package links

import (
	"context"
	"log"
	"log/slog"
	"testing"
	"time"

	"github.com/IvanDrf/checker/internal/models"
	linkService "github.com/IvanDrf/checker/internal/service/links"
	checker_api "github.com/IvanDrf/link-checker/pkg/checker-api"

	"github.com/alicebob/miniredis"
	"github.com/redis/go-redis/v9"
	"github.com/stretchr/testify/assert"
)

const testingCheckLinksTime = 5 * time.Second

func setUpRedisCLient() *redis.Client {
	mRedis, err := miniredis.Run()
	if err != nil {
		log.Fatal(err)
	}

	return redis.NewClient(&redis.Options{
		Addr: mRedis.Addr(),
	})
}

var (
	rdb   = setUpRedisCLient()
	links = checker_api.CheckRequest{
		Links: []string{
			"vk.com",
			"ya.ru",
			"google.com",

			"1",
			"https://httpbin.org/status/404",
			"https://httpbin.org/status/500",
		},
	}

	expected = map[string]models.Link{
		"vk.com": {
			Link:   "vk.com",
			Status: true,
		},

		"ya.ru": {
			Link:   "ya.ru",
			Status: true,
		},

		"google.com": {
			Link:   "google.com",
			Status: true,
		},

		"1": {
			Link:   "1",
			Status: false,
		},

		"https://httpbin.org/status/404": {
			Link:   "https://httpbin.org/status/404",
			Status: false,
		},

		"https://httpbin.org/status/500": {
			Link:   "https://httpbin.org/status/500",
			Status: false,
		},
	}
)

func TestGrpcCheckLinks(t *testing.T) {
	s := &serverAPI{
		linkChecker: linkService.NewLinkChecker(rdb, slog.Default()),
		logger:      slog.Default(),
	}

	ctx, cancel := context.WithTimeout(context.Background(), testingCheckLinksTime)
	defer cancel()

	resp, err := s.CheckLinks(ctx, &links)

	assert.Nil(t, err)

	for _, link := range resp.Links {
		assert.Equal(t, expected[link.GetLink()].Link, link.GetLink())
		assert.Equal(t, expected[link.GetLink()].Status, link.GetStatus())
	}
}
