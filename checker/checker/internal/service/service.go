package service

import (
	"checker/checker/internal/models"
	"context"
)

type LinkChecker interface {
	CheckLinks(ctx context.Context, links []string) []models.Link
}
