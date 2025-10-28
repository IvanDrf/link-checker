package service

import (
	"context"

	"github.com/IvanDrf/checker/internal/models"
)

const MaxLinksCount = 100

type LinkChecker interface {
	CheckLinks(ctx context.Context, links []string) []models.Link
}
