package middleware

import (
	"encoding/json"
	"log/slog"
	"net/http"

	"github.com/IvanDrf/api-gateway/internal/config"
	"github.com/IvanDrf/api-gateway/internal/errs"
	"github.com/IvanDrf/api-gateway/internal/transport/jwt"
)

type Auth interface {
	AuthMiddleware(next http.HandlerFunc) http.HandlerFunc
}

type authMiddleware struct {
	jwter jwt.JWTer

	logger *slog.Logger
}

func newAuthMiddleware(cfg *config.Config, log *slog.Logger) Auth {
	return &authMiddleware{
		jwter:  jwt.NewJWTer(cfg),
		logger: log,
	}
}

func (a *authMiddleware) AuthMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		a.logger.Debug("auth_middle -> start")

		accessToken, err := a.jwter.GetToken(jwt.AccessToken, r)
		if err != nil {
			a.logger.Debug("auth_middle -> cant get token")

			w.WriteHeader(errs.GetCode(err))
			json.NewEncoder(w).Encode(err)
			return
		}

		err = a.jwter.IsValid(accessToken)
		if err != nil {
			a.logger.Debug("auth_middle -> given invalid token")

			w.WriteHeader(errs.GetCode(err))
			json.NewEncoder(w).Encode(err)
			return
		}

		a.logger.Debug("auth_middle -> success")
		next(w, r)
	}
}
