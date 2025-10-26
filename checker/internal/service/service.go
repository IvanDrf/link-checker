package service

import (
	"context"
	"github.com/IvanDrf/checker/internal/models"
)

type LinkChecker interface {
	CheckLinks(ctx context.Context, links []string) []models.Link
}
