package main

import (
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"

	"github.com/IvanDrf/auth/internal/config"
	"github.com/IvanDrf/auth/logger"

	"github.com/IvanDrf/auth/internal/app"
)

func main() {
	cfg := config.MustLoad()
	logger := logger.InitLogger(cfg.LoggerLevel)

	application := app.New(cfg, logger)
	go func() {
		if err := application.Run(); err != nil {
			log.Fatal(err)
		}
	}()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGTERM, syscall.SIGINT)

	<-stop
	logger.Info(fmt.Sprintf("shutdown _AUTH_ server on %s", cfg.GRPC.Port))
	application.Stop()
}
