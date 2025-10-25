package api

import (
	"api-gateway/internal/config"
	"api-gateway/internal/errs"
	"api-gateway/internal/models"
	"api-gateway/internal/transport/api/response"
	"checker/protos/gen-go/checkerv1"
	"context"
	"encoding/json"
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
	w.Header().Set(contentType, jsonContent)

	if r.Header.Get(contentType) != jsonContent {
		response.RespondUnsupportedMedia(w)

		return
	}
	defer r.Body.Close()

	links := models.Links{}
	err := json.NewDecoder(r.Body).Decode(&links)
	if err != nil {
		response.RespondBadRequest(w)

		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), CtxTime)
	defer cancel()

	resp, err := c.checkerClient.CheckLinks(ctx, &checkerv1.CheckRequest{
		Links: links.Links,
	})
	if err != nil {
		errs.HandlerGrpcError(w, err)
		return
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(convertToLinks(resp))
}

func convertToLinks(grpcResp *checkerv1.CheckResponse) []models.Link {
	links := make([]models.Link, 0, len(grpcResp.Links))

	for i := range grpcResp.Links {
		links = append(links, models.Link{
			Link:   grpcResp.Links[i].Link,
			Status: grpcResp.Links[i].Status,
		})
	}

	return links
}
