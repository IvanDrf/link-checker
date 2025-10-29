package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/IvanDrf/api-gateway/internal/app"
	"github.com/IvanDrf/api-gateway/internal/config"
	"github.com/IvanDrf/api-gateway/logger"
)

func main() {
	cfg := config.MustLoad()
	logger := logger.InitLogger(cfg)

	app := app.New(cfg, logger)
	go app.Run()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGABRT, syscall.SIGTERM, syscall.SIGINT)

	<-stop
	logger.Info(fmt.Sprintf("shutdown _API_ server on %s", cfg.Api.Port))
	app.Stop()
}
