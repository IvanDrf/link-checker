package api

import (
	"api-gateway/internal/config"
	"auth/protos/gen-go/authv1"
	"checker/protos/gen-go/checkerv1"
	"fmt"
	"log"

	"google.golang.org/grpc"
)

type apiGateway struct {
	auth     authv1.AuthClient
	authConn *grpc.ClientConn

	checker     checkerv1.CheckerClient
	checkerConn *grpc.ClientConn
}

func NewAPIGateway(cfg *config.Config) *apiGateway {
	authConn, err := grpc.NewClient(fmt.Sprintf("%s:%d", cfg.Auth.Addr, cfg.Auth.Port))
	if err != nil {
		log.Fatal("auth: ", err)
	}

	checkerConn, err := grpc.NewClient(fmt.Sprintf("%s:%d", cfg.Checker.Addr, cfg.Checker.Port))
	if err != nil {
		log.Fatal("checker: ", err)
	}

	return &apiGateway{
		auth:     authv1.NewAuthClient(authConn),
		authConn: authConn,

		checker:     checkerv1.NewCheckerClient(checkerConn),
		checkerConn: checkerConn,
	}
}

func (a *apiGateway) Close() {
	if a.authConn != nil {
		a.authConn.Close()
	}

	if a.checkerConn != nil {
		a.checkerConn.Close()
	}
}
