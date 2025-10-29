package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/IvanDrf/checker/internal/app"
	"github.com/IvanDrf/checker/internal/config"
	"github.com/IvanDrf/checker/internal/database"
	logger "github.com/IvanDrf/checker/logger"
)

func main() {
	cfg := config.MustLoad()
	logger := logger.InitLogger(cfg.LoggerLevel)

	rdb := database.InitRedisDatabase(cfg)
	defer rdb.Close()

	app := app.New(cfg, rdb, logger)

	go app.Run()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGABRT, syscall.SIGTERM, syscall.SIGINT)

	<-stop
	logger.Info(fmt.Sprintf("shutdown _CHECKER_ server on %s", cfg.GRPC.Port))
	app.Stop()
}
