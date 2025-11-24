package config

import (
	"flag"
	"log"
	"os"

	"github.com/IvanDrf/api-gateway/internal/errs"

	"github.com/ilyakaznacheev/cleanenv"
)

type Config struct {
	Env   string `yaml:"env"`
	Level string `yaml:"level"`

	Api     ApiConfig     `yaml:"api"`
	Auth    AuthConfig    `yaml:"auth"`
	Checker CheckerConfig `yaml:"checker"`

	Email EmailConfig `yaml:"email"`
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

type EmailConfig struct {
	HostAddr string `yaml:"host_addr"`
	Username string `yaml:"username"`
	Password string `yaml:"password"`
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
