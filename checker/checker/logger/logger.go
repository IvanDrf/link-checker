package logger

import (
	"checker/checker/internal/config"
	"log"
	"log/slog"
	"os"
)

func InitLogger(cfg *config.Config) *slog.Logger {
	level := setLoggerLevel(cfg.Level)
	return slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{
		Level:     level,
		AddSource: false,
	}))
}

const (
	debugLevel = "debug"
	infoLevel  = "info"
	warnLevel  = "warn"
	errorLevel = "error"
)

func setLoggerLevel(level string) slog.Leveler {
	switch level {
	case debugLevel:
		return slog.LevelDebug

	case infoLevel:
		return slog.LevelInfo

	case warnLevel:
		return slog.LevelWarn

	case errorLevel:
		return slog.LevelError

	default:
		log.Fatal("can't setup logger level, bad cfg")
		return nil
	}
}
