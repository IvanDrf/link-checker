package config

import (
	"flag"
	"log"
	"os"

	"github.com/ilyakaznacheev/cleanenv"
)

type Config struct {
	Env         string `yaml:"env"`
	LoggerLevel string `yaml:"level"`

	GRPC  GRPCConfig  `yaml:"grpc"`
	Redis RedisConfig `yaml:"redis"`
}

type GRPCConfig struct {
	Port string `yaml:"port" `
}

type RedisConfig struct {
	Host string `yaml:"host"`
	Port string `yaml:"port"`

	Password string `yaml:"password"`
}

const defaultPath = "../checker/config/config.yaml"

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

func getPathFromFlag() string {
	cfgPath := ""

	flag.StringVar(&cfgPath, "cfg", "", "")
	flag.Parse()

	return cfgPath
}
