package middleware

import (
	"github.com/IvanDrf/api-gateway/internal/config"
	"log/slog"
)

type Middleware interface {
	Auth
}

type middleware struct {
	Auth
}

func NewMiddleware(cfg *config.Config, logger *slog.Logger) Middleware {
	return &middleware{
		newAuthMiddleware(cfg, logger),
	}
}
