package repo

import (
	"context"
)

type CacheRepo interface {
	SaveLinks(ctx context.Context, links *[]interface{}) error
	GetLink(ctx context.Context, link string) (bool, error)
}
