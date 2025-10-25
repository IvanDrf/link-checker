package api

import (
	"api-gateway/internal/config"
	"api-gateway/internal/errs"
	"api-gateway/internal/models"
	"api-gateway/internal/transport/api/response"
	"api-gateway/internal/transport/cookies"
	"api-gateway/internal/transport/jwt"
	"auth/protos/gen-go/authv1"
	"context"
	"encoding/json"
	"fmt"
	"log"
	"log/slog"
	"net/http"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

const (
	contentType = "Content-Type"
	jsonContent = "application/json"
)

type authGateway struct {
	authClient authv1.AuthClient
	authConn   *grpc.ClientConn

	jwter   jwt.JWTer
	cookier cookies.Cookier

	log *slog.Logger
}

func newAuthGateway(cfg *config.Config, logger *slog.Logger) AuthGateway {
	authClient, authConn := connectToAuth(cfg)

	return &authGateway{
		authClient: authClient,
		authConn:   authConn,

		jwter:   jwt.NewJWTer(cfg),
		cookier: cookies.NewCookier(),

		log: logger,
	}

}

func connectToAuth(cfg *config.Config) (authv1.AuthClient, *grpc.ClientConn) {
	authConn, err := grpc.NewClient(fmt.Sprintf("%s:%d", cfg.Auth.Addr, cfg.Auth.Port), grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatal("auth: ", err)
	}

	return authv1.NewAuthClient(authConn), authConn
}

func (a *authGateway) CloseAuth() {
	if a.authConn != nil {
		a.authConn.Close()
	}
}

func (a *authGateway) Register(w http.ResponseWriter, r *http.Request) {
	w.Header().Set(contentType, jsonContent)

	if r.Header.Get(contentType) != jsonContent {
		response.RespondUnsupportedMedia(w)

		return
	}
	defer r.Body.Close()

	user := models.User{}
	err := json.NewDecoder(r.Body).Decode(&user)
	if err != nil || user.Email == "" || user.Password == "" {
		response.RespondBadRequest(w)

		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), CtxTime)
	defer cancel()

	resp, err := a.authClient.Register(ctx, &authv1.RegisterRequest{
		Email:    user.Email,
		Password: user.Password,
	})

	if err != nil {
		w.WriteHeader(http.StatusUnauthorized)

		json.NewEncoder(w).Encode(err)
		return
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(resp)
}

func (a *authGateway) Login(w http.ResponseWriter, r *http.Request) {
	w.Header().Set(contentType, jsonContent)

	if r.Header.Get(contentType) != jsonContent {
		response.RespondUnsupportedMedia(w)

		return
	}
	defer r.Body.Close()

	user := models.User{}
	err := json.NewDecoder(r.Body).Decode(&user)
	if err != nil || user.Email == "" || user.Password == "" {
		response.RespondBadRequest(w)

		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), CtxTime)
	defer cancel()

	resp, err := a.authClient.Login(ctx, &authv1.LoginRequest{
		Email:    user.Email,
		Password: user.Password,
	})
	if err != nil {
		errs.HandlerGrpcError(w, err)
		return
	}

	a.cookier.SetAuthCookies(w, resp.Access, resp.Refresh)

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(models.Tokens{
		Access:  resp.Access,
		Refresh: resp.Refresh,
	})
}

func (a *authGateway) RefreshTokens(w http.ResponseWriter, r *http.Request) {
	w.Header().Set(contentType, jsonContent)

	refresh, err := a.jwter.GetToken(jwt.RefreshToken, r)
	if err != nil {
		w.WriteHeader(http.StatusUnauthorized)
		json.NewEncoder(w).Encode(err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), CtxTime)
	defer cancel()

	resp, err := a.authClient.RefreshTokens(ctx, &authv1.RefreshRequest{
		Refresh: refresh,
	})
	if err != nil {
		errs.HandlerGrpcError(w, err)

		return
	}

	a.cookier.SetAuthCookies(w, resp.Access, resp.Refresh)

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(models.Tokens{
		Access:  resp.Access,
		Refresh: resp.Refresh,
	})
}
