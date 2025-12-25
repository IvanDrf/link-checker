package app

import (
	"database/sql"
	"fmt"
	"log/slog"
	"net"

	"github.com/IvanDrf/auth/internal/config"
	"github.com/IvanDrf/auth/internal/database"
	"github.com/IvanDrf/auth/internal/errs"
	auth "github.com/IvanDrf/auth/internal/grpc"
	"github.com/redis/go-redis/v9"

	"google.golang.org/grpc"
)

type App struct {
	gRPCserver *grpc.Server
	port       string

	db  *sql.DB
	rdb *redis.Client

	logger *slog.Logger
}

func New(cfg *config.Config, log *slog.Logger) *App {
	gRPCServer := grpc.NewServer()

	app := &App{
		gRPCserver: gRPCServer,
		port:       cfg.GRPC.Port,

		db:  database.InitDatabase(cfg),
		rdb: database.InitRedisDatabase(cfg),

		logger: log,
	}

	auth.Register(gRPCServer, cfg, app.db, app.rdb, log)
	return app
}

func (a *App) Run() error {
	l, err := net.Listen("tcp", fmt.Sprintf(":%s", a.port))
	if err != nil {
		return errs.ErrCantConnectToTCP(err)
	}

	a.logger.Info(fmt.Sprintf("starting _AUTH_ server on %s", a.port))
	if err := a.gRPCserver.Serve(l); err != nil {
		return errs.ErrCantStartAuthServer(err)
	}

	return nil
}

func (a *App) Stop() {
	defer a.db.Close()
	defer a.rdb.Close()

	a.gRPCserver.GracefulStop()
}
