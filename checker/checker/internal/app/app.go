package app

import (
	"checker/checker/internal/config"
	checker "checker/checker/internal/grpc"
	"errors"
	"fmt"
	"log/slog"
	"net"

	"github.com/redis/go-redis/v9"
	"google.golang.org/grpc"
)

type App struct {
	gRPCserver *grpc.Server
	port       string

	log *slog.Logger
}

func New(cfg *config.Config, rdb *redis.Client, logger *slog.Logger) *App {
	gRPCServer := grpc.NewServer()

	app := &App{
		gRPCserver: gRPCServer,
		port:       cfg.GRPC.Port,
		log:        logger,
	}

	checker.Register(gRPCServer, cfg, rdb, logger)
	return app
}

func (a *App) Run() error {
	l, err := net.Listen("tcp", fmt.Sprintf(":%s", a.port))
	if err != nil {
		return errors.New("")
	}

	a.log.Info(fmt.Sprintf("starting _CHECKER_ server on %s", a.port))
	if err := a.gRPCserver.Serve(l); err != nil {
		return fmt.Errorf("")
	}

	return nil
}

func (a *App) Stop() {
	a.gRPCserver.GracefulStop()
}
