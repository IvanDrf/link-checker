package redisCache

import (
	"context"
	"log"
	"testing"
	"time"

	"github.com/alicebob/miniredis"
	"github.com/redis/go-redis/v9"
	"github.com/stretchr/testify/assert"
)

const testingRepoTime = 5 * time.Second

func setUpRedisClient() *redis.Client {
	mRedist, err := miniredis.Run()
	if err != nil {
		log.Fatal(err)
	}

	return redis.NewClient(
		&redis.Options{
			Addr: mRedist.Addr(),
		},
	)
}

var (
	rdb = setUpRedisClient()

	links = []interface{}{
		"first.com",
		true,

		"second.com",
		true,

		"third.com",
		false,
	}
)

func TestSaveLinks(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), testingRepoTime)
	defer cancel()

	repo := NewCacheRepo(rdb)
	assert.Nil(t, repo.SaveLinks(ctx, &links))
}

func TestGetLink(t *testing.T) {
	errLink := "not-in-redis"

	ctx, cancel := context.WithTimeout(context.Background(), testingRepoTime)
	defer cancel()

	repo := NewCacheRepo(rdb)
	for i := 0; i < len(links); i += 2 {
		status, err := repo.GetLink(ctx, links[i].(string))

		assert.Nil(t, err)
		assert.Equal(t, links[i+1].(bool), status)
	}

	status, err := repo.GetLink(ctx, errLink)
	assert.NotNil(t, err)
	assert.False(t, status)
}
