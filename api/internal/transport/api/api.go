package api

import (
	"github.com/IvanDrf/api-gateway/internal/config"
	"log/slog"
	"net/http"
	"time"
)

const (
	CtxTime = 5 * time.Second
)

type ApiGateway interface {
	AuthGateway
	CheckerGateway
}

type AuthGateway interface {
	Register(w http.ResponseWriter, r *http.Request)
	Login(w http.ResponseWriter, r *http.Request)
	RefreshTokens(w http.ResponseWriter, r *http.Request)

	CloseAuth()
}

type CheckerGateway interface {
	CheckLinks(w http.ResponseWriter, r *http.Request)

	CloseChecker()
}

type apiGateway struct {
	AuthGateway
	CheckerGateway
}

func NewApiGateway(cfg *config.Config, logger *slog.Logger) ApiGateway {
	return &apiGateway{
		AuthGateway:    newAuthGateway(cfg, logger),
		CheckerGateway: newCheckerGateway(cfg, logger),
	}
}
