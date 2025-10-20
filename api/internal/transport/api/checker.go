package api

import (
	"api-gateway/internal/config"
	"checker/protos/gen-go/checkerv1"
	"fmt"
	"log"
	"log/slog"
	"net/http"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type checkerGateway struct {
	checkerClient checkerv1.CheckerClient
	checkerConn   *grpc.ClientConn

	log *slog.Logger
}

func newCheckerGateway(cfg *config.Config, logger *slog.Logger) CheckerGateway {
	checkerClient, checkerConn := connectToChecker(cfg)

	return &checkerGateway{
		checkerClient: checkerClient,
		checkerConn:   checkerConn,
	}

}

func connectToChecker(cfg *config.Config) (checkerv1.CheckerClient, *grpc.ClientConn) {
	checkerConn, err := grpc.NewClient(fmt.Sprintf("%s:%d", cfg.Checker.Addr, cfg.Checker.Port), grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatal("checker: ", err)
	}

	return checkerv1.NewCheckerClient(checkerConn), checkerConn
}

func (a *checkerGateway) CloseChecker() {
	if a.checkerConn != nil {
		a.checkerConn.Close()
	}
}

func (c *checkerGateway) CheckLinks(w http.ResponseWriter, r *http.Request) {

}
