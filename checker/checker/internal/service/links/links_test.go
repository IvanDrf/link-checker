package linkService

import (
	"checker/checker/internal/models"
	"context"
	"log"
	"log/slog"
	"testing"
	"time"

	"github.com/alicebob/miniredis"
	"github.com/redis/go-redis/v9"
	"github.com/stretchr/testify/assert"
)

const testingServiceTime = 5 * time.Second

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
	rdb = setUpRedisCLient()

	links = []string{
		"vk.com",
		"ya.ru",
		"google.com",

		"1",
		"https://httpbin.org/status/404",
		"https://httpbin.org/status/500",
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

func TestNotCheckedLinks(t *testing.T) {
	results := testCheckerService()

	for _, result := range results {
		assert.Equal(t, expected[result.Link].Link, result.Link)
		assert.Equal(t, expected[result.Link].Status, result.Status)

		assert.True(t, result.Checked)
	}
}

func TestCheckedLinks(t *testing.T) {
	time.Sleep(1 * time.Second) // waiting for links to be saved in redis

	results := testCheckerService()

	for _, result := range results {
		assert.Equal(t, expected[result.Link].Link, result.Link)
		assert.Equal(t, expected[result.Link].Status, result.Status)

		assert.False(t, result.Checked)
	}
}

func testCheckerService() []models.Link {
	ctx, cancel := context.WithTimeout(context.Background(), testingServiceTime)
	defer cancel()

	service := NewLinkChecker(rdb, slog.Default())
	return service.CheckLinks(ctx, links)
}
