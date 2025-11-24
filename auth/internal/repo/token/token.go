package tokenRepo

import (
	"context"
	"time"

	"github.com/IvanDrf/auth/internal/errs"
	"github.com/IvanDrf/auth/internal/repo"
	"github.com/redis/go-redis/v9"
)

const timeToLive = 15 * time.Minute

type tokenRepo struct {
	rdb *redis.Client
}

func NewTokenRepo(rdb *redis.Client) repo.TokenRepo {
	return &tokenRepo{
		rdb: rdb,
	}
}

func (r *tokenRepo) AddToken(ctx context.Context, token, email string) error {
	err := r.rdb.Set(ctx, token, email, timeToLive).Err()

	return err
}

func (r *tokenRepo) GetEmailByToken(ctx context.Context, token string) (string, error) {
	email, err := r.rdb.Get(ctx, token).Result()
	if err != redis.Nil {
		return "", errs.ErrVerifTokenDoesntExist(token)
	}

	if err != nil {
		return "", errs.ErrCantGetVerifTokenFromRedis(token)
	}

	return email, nil
}
