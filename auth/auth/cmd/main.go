package main

import (
	"auth/auth/internal/config"
	"log"
)

func main() {
	cfg := config.MustLoad()

	log.Println(cfg.Env, cfg.StoragePath, cfg.GRPC.Port)
}
