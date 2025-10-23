package main

import (
	"checker/checker/internal/app"
	"checker/checker/internal/config"
	"checker/checker/internal/database"
	logger "checker/checker/logger"
	"fmt"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	cfg := config.MustLoad()
	log := logger.InitLogger(cfg.LoggerLevel)
	rdb := database.InitRedisDatabase(cfg)

	defer rdb.Close()

	app := app.New(cfg, rdb, log)

	go app.Run()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGABRT, syscall.SIGTERM, syscall.SIGINT)

	<-stop
	log.Info(fmt.Sprintf("shutdown _CHECKER_ server on %s", cfg.GRPC.Port))
	app.Stop()
}
