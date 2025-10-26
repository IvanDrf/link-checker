package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/IvanDrf/auth/internal/config"
	"github.com/IvanDrf/auth/logger"

	"github.com/IvanDrf/auth/internal/app"
)

func main() {
	cfg := config.MustLoad()
	log := logger.InitLogger(cfg.LoggerLevel)

	application := app.New(cfg, log)
	go application.Run()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGTERM, syscall.SIGINT)

	<-stop
	log.Info(fmt.Sprintf("shutdown _AUTH_ server on %s", cfg.GRPC.Port))
	application.Stop()
}
