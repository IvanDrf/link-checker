package api

import (
	"api-gateway/internal/config"
	"api-gateway/internal/errs"
	"api-gateway/internal/models"
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
	jsonContent = "application/json"
)

type authGateway struct {
	authClient authv1.AuthClient
	authConn   *grpc.ClientConn

	log *slog.Logger
}

func newAuthGateway(cfg *config.Config, logger *slog.Logger) AuthGateway {
	authClient, authConn := connectToAuth(cfg)

	return &authGateway{
		authClient: authClient,
		authConn:   authConn,

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
	w.Header().Set("Content-Type", jsonContent)

	if r.Header.Get("Content-Type") != jsonContent {
		w.WriteHeader(http.StatusUnsupportedMediaType)

		json.NewEncoder(w).Encode(errs.ErrUnsupportedMediaType())
		return
	}
	defer r.Body.Close()

	user := models.User{}
	err := json.NewDecoder(r.Body).Decode(&user)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)

		json.NewEncoder(w).Encode(errs.ErrInvalidJSON())
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

		json.NewEncoder(w).Encode(err.Error())
		return
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(resp)
}

func (a *authGateway) Login(w http.ResponseWriter, r *http.Request)         {}
func (a *authGateway) RefreshTokens(w http.ResponseWriter, r *http.Request) {}
