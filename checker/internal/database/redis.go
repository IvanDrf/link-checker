package database

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/IvanDrf/checker/internal/config"

	"github.com/redis/go-redis/v9"
)

const redisConnectionTime = 2 * time.Second

func InitRedisDatabase(cfg *config.Config) *redis.Client {
	db := redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%s", cfg.Redis.Host, cfg.Redis.Port),
		Password: cfg.Redis.Password,
		DB:       cfg.Redis.DB,
	})

	ctx, cancel := context.WithTimeout(context.Background(), redisConnectionTime)
	defer cancel()

	_, err := db.Ping(ctx).Result()
	if err != nil {
		log.Fatal(err)
	}

	return db
}
