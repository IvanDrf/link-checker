package app

import (
	"auth/auth/internal/config"
	auth "auth/auth/internal/grpc"
	"errors"
	"fmt"
	"log/slog"
	"net"

	"google.golang.org/grpc"
)

type App struct {
	gRPCserver *grpc.Server
	port       string

	storagePath string

	log *slog.Logger
}

func New(cfg *config.Config, log *slog.Logger) *App {
	gRPCServer := grpc.NewServer()
	auth.Register(gRPCServer)

	return &App{
		gRPCserver:  gRPCServer,
		port:        cfg.GRPC.Port,
		storagePath: cfg.StoragePath,
		log:         log,
	}
}

func (a *App) Run() error {
	l, err := net.Listen("tcp", fmt.Sprintf(":%s", a.port))
	if err != nil {
		return errors.New("")
	}

	a.log.Info(fmt.Sprintf("starting server on %s", a.port))
	if err := a.gRPCserver.Serve(l); err != nil {
		return fmt.Errorf("")
	}

	return nil
}

func (a *App) Stop() {
	a.gRPCserver.GracefulStop()
}
