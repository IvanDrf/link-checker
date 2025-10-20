package config

import (
	"api-gateway/internal/errs"
	"flag"
	"log"
	"os"

	"github.com/ilyakaznacheev/cleanenv"
)

type Config struct {
	Env   string `yaml:"env"`
	Level string `yaml:"level"`

	Api     ApiConfig     `yaml:"api"`
	Auth    AuthConfig    `yaml:"auth"`
	Checker CheckerConfig `yaml:"checker"`
}

type ApiConfig struct {
	Addr string `yaml:"addr"`
	Port string `yaml:"port"`
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
		log.Fatal(errs.ErrCantFindConfigFile(cfgPath))
	}

	cfg := new(Config)
	if err := cleanenv.ReadConfig(cfgPath, cfg); err != nil {
		log.Fatal(errs.ErrCantParseConfigFile(err))
	}

	return cfg
}

const flagCfg = "cfg"

func getPathFromFlag() string {
	cfgPath := ""

	flag.StringVar(&cfgPath, flagCfg, "", "")
	flag.Parse()

	return cfgPath
}
