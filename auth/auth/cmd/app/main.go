package main

import (
	"auth/auth/internal/app"
	"auth/auth/internal/config"
	"auth/auth/logger"
	"fmt"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	cfg := config.MustLoad()
	log := logger.InitLogger(cfg.LoggerLevel)

	application := app.New(cfg, log)
	go application.Run()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGTERM, syscall.SIGINT)

	<-stop
	log.Info(fmt.Sprintf("shutdown server on %s", cfg.GRPC.Port))
	application.Stop()
}
