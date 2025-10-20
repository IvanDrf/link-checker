package app

import (
	"api-gateway/internal/config"
	"api-gateway/internal/transport/server"
	"context"
	"log/slog"
	"time"
)

type App struct {
	server server.Server
}

func New(cfg *config.Config, logger *slog.Logger) *App {
	return &App{
		server: *server.NewServer(cfg, logger),
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
