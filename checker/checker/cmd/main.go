package main

import (
	logger "checker/checker"
	"checker/checker/internal/app"
	"checker/checker/internal/config"
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
	app.Stop()
}
