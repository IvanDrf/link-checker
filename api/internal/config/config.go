package config

import (
	"flag"
	"log"
	"os"

	"github.com/ilyakaznacheev/cleanenv"
)

type Config struct {
	Env   string `yaml:"env"`
	Level string `yaml:"level"`

	Auth    AuthConfig    `yaml:"auth"`
	Checker CheckerConfig `yaml:"checker"`
}

type AuthConfig struct {
	Addr string    `yaml:"addr"`
	Port int       `yaml:"port"`
	JWT  JWTConfig `yaml:"jwt"`
}

type JWTConfig struct {
	Key string `yaml:"key"`
}

type CheckerConfig struct {
	Addr string `yaml:"addr"`
	Port int    `yaml:"port"`
}

const defaultPath = "config/config.yaml"

func MustLoad() *Config {
	cfgPath := getPathFromFlag()
	if cfgPath == "" {
		cfgPath = defaultPath
	}

	if _, err := os.Stat(cfgPath); os.IsExist(err) {
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
