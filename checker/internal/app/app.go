package app

import (
	"errors"
	"fmt"
	"log/slog"
	"net"

	"github.com/IvanDrf/checker/internal/config"
	checker "github.com/IvanDrf/checker/internal/grpc"
	"github.com/IvanDrf/checker/internal/messages"
	"github.com/IvanDrf/checker/internal/messages/rabbitmq"

	"github.com/redis/go-redis/v9"
	"google.golang.org/grpc"
)

type App struct {
	gRPCserver *grpc.Server
	port       string

	messenger messages.Messenger

	logger *slog.Logger
}

func New(cfg *config.Config, rdb *redis.Client, logger *slog.Logger) *App {
	gRPCServer := grpc.NewServer()

	app := &App{
		gRPCserver: gRPCServer,
		port:       cfg.GRPC.Port,
		messenger:  rabbitmq.NewRabbiter(cfg, rdb, logger),
		logger:     logger,
	}

	checker.Register(gRPCServer, cfg, rdb, logger)
	return app
}

func (a *App) Run() error {
	a.startRabbitmq()

	l, err := net.Listen("tcp", fmt.Sprintf(":%s", a.port))
	if err != nil {
		return errors.New("")
	}

	a.logger.Info(fmt.Sprintf("starting _CHECKER_ server on %s", a.port))
	if err := a.gRPCserver.Serve(l); err != nil {
		return fmt.Errorf("")
	}

	return nil
}

func (a *App) startRabbitmq() {
	go a.messenger.ReadMessages()
	go a.messenger.ServiceMessages()
	go a.messenger.SendMessages()
}

func (a *App) Stop() {
	a.gRPCserver.GracefulStop()
	a.messenger.GracefulStop()
}
