package redisCache

import (
	"checker/checker/internal/errs"
	"checker/checker/internal/models"
	"checker/checker/internal/repo"
	"context"
	"time"

	"github.com/redis/go-redis/v9"
)

const timeToLive = 5 * time.Minute

type cacheRepo struct {
	rdb *redis.Client
}

func NewCacheRepo(rdb *redis.Client) repo.CacheRepo {
	return &cacheRepo{rdb: rdb}
}

func (c *cacheRepo) SaveLink(ctx context.Context, link *models.Link) error {
	err := c.rdb.Set(ctx, link.Link, link.Status, timeToLive).Err()
	if err != nil {
		return errs.ErrCantAddLink(&link.Link)
	}

	return nil
}

func (c *cacheRepo) GetLink(ctx context.Context, link string) (bool, error) {
	linkStatus, err := c.rdb.Get(ctx, link).Result()
	if err == redis.Nil {
		return false, errs.ErrLinkNotInRedis()
	}

	if err != nil {
		return false, errs.ErrCantGetLink()
	}

	return linkStatus == "true", nil
}
