package app

import (
	"errors"
	"fmt"
	"log/slog"
	"net"

	"github.com/IvanDrf/checker/internal/config"
	checker "github.com/IvanDrf/checker/internal/grpc"
	"github.com/IvanDrf/checker/internal/rabbitmq"

	"github.com/redis/go-redis/v9"
	"google.golang.org/grpc"
)

type App struct {
	gRPCserver *grpc.Server
	port       string

	rabbiter rabbitmq.Rabbiter

	log *slog.Logger
}

func New(cfg *config.Config, rdb *redis.Client, logger *slog.Logger) *App {
	gRPCServer := grpc.NewServer()

	app := &App{
		gRPCserver: gRPCServer,
		port:       cfg.GRPC.Port,
		rabbiter:   rabbitmq.NewRabbiter(cfg, rdb, logger),
		log:        logger,
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

	a.log.Info(fmt.Sprintf("starting _CHECKER_ server on %s", a.port))
	if err := a.gRPCserver.Serve(l); err != nil {
		return fmt.Errorf("")
	}

	return nil
}

func (a *App) startRabbitmq() {
	go a.rabbiter.ReadMessages()
	go a.rabbiter.ServiceMessages()
	go a.rabbiter.SendMessages()
}

func (a *App) Stop() {
	a.gRPCserver.GracefulStop()
	a.rabbiter.GracefulStop()
}
