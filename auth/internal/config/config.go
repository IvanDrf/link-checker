package config

import (
	"flag"
	"log"
	"os"
	"time"

	"github.com/ilyakaznacheev/cleanenv"
)

type Config struct {
	Env         string `yaml:"env" `
	LoggerLevel string `yaml:"level"`
	StoragePath string `yaml:"storage_path" `

	GRPC  GRPCConfig  `yaml:"grpc" `
	JWT   JWTConfig   `yaml:"jwt"`
	Email EmailConfig `yaml:"email"`
}

type GRPCConfig struct {
	Port string `yaml:"port" `
}

type JWTConfig struct {
	Key string `yaml:"key"`

	AccessExpTime  time.Duration `yaml:"access_exp_time"`
	RefreshExpTime time.Duration `yaml:"refresh_exp_time"`
}

type EmailConfig struct {
	HostAddr string `yaml:"host_addr"`
	Username string `yaml:"username"`
	Password string `yaml:"password"`
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

func getPathFromFlag() string {
	cfgPath := ""

	flag.StringVar(&cfgPath, "cfg", "", "")
	flag.Parse()

	return cfgPath
}
