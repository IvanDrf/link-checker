package main

import (
	"checker/checker/internal/app"
	"checker/checker/internal/config"
	logger "checker/checker/logger"
	"fmt"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	cfg := config.MustLoad()
	log := logger.InitLogger(cfg)

	app := app.New(cfg, log)

	go app.Run()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGABRT, syscall.SIGTERM, syscall.SIGINT)

	<-stop
	log.Info(fmt.Sprintf("shutdown server on %s", cfg.GRPC.Port))
	app.Stop()
}
