package middleware

import (
	"log/slog"

	"github.com/IvanDrf/api-gateway/internal/config"
)

type Middleware interface {
	Auth
}

type middleware struct {
	Auth
}

func NewMiddleware(cfg *config.Config, logger *slog.Logger) Middleware {
	return &middleware{
		Auth: newAuthMiddleware(cfg, logger),
	}
}
