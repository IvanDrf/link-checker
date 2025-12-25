package app

import (
	"context"
	"log/slog"
	"time"

	"github.com/IvanDrf/api-gateway/internal/config"
	"github.com/IvanDrf/api-gateway/internal/transport/server"
)

type App struct {
	server *server.Server
}

func New(cfg *config.Config, logger *slog.Logger) *App {
	return &App{
		server: server.NewServer(cfg, logger),
	}
}

func (a *App) Run() {
	a.server.RegisterRoutes()
	a.server.StartServer()
}

const shutdownTime = 3 * time.Second

func (a *App) Stop() {
	ctx, cancel := context.WithTimeout(context.Background(), shutdownTime)
	defer cancel()

	a.server.GracefulStop(ctx)
}
