package main

import (
	"api-gateway/internal/config"
	"log"
)

func main() {
	cfg := config.MustLoad()

	log.Println(cfg)
}
