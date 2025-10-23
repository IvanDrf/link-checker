package repo

import (
	"checker/checker/internal/models"
	"context"
)

type CacheRepo interface {
	SaveLink(ctx context.Context, link *models.Link) error
	GetLink(ctx context.Context, link string) (bool, error)
}
