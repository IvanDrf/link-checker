package config

import (
	"flag"
	"log"
	"os"

	"github.com/ilyakaznacheev/cleanenv"
)

type Config struct {
	Env         string     `yaml:"env" `
	Level       string     `yaml:"level"`
	StoragePath string     `yaml:"storage_path" `
	GRPC        GRPCConfig `yaml:"grpc" `
}

type GRPCConfig struct {
	Port string `yaml:"port" `
}

const defaultPath = "../auth/config/config.yaml"

func MustLoad() *Config {
	cfgPath := getPathFromFlag()
	if cfgPath == "" {
		cfgPath = defaultPath
	}

	if _, err := os.Stat(cfgPath); os.IsNotExist(err) {
		log.Fatal("cant find config file " + cfgPath)
	}

	cfg := new(Config)

	if err := cleanenv.ReadConfig(cfgPath, cfg); err != nil {
		log.Fatal("cant parse config file " + err.Error())
	}

	return cfg
}

const cfg = "cfg"

func getPathFromFlag() string {
	cfgPath := ""

	flag.StringVar(&cfgPath, cfg, "", "")
	flag.Parse()

	return cfgPath
}
