package server

import (
	"api-gateway/internal/config"
	"api-gateway/internal/errs"
	"api-gateway/internal/transport/api"
	"api-gateway/internal/transport/middleware"
	"context"
	"fmt"
	"log"
	"log/slog"
	"net/http"
)

type Server struct {
	httpServer *http.Server
	mux        *http.ServeMux
	api        api.ApiGateway
	middle     middleware.Middleware

	log *slog.Logger
}

func NewServer(cfg *config.Config, logger *slog.Logger) *Server {
	addr := cfg.Api.Addr + ":" + cfg.Api.Port

	return &Server{
		httpServer: &http.Server{
			Addr: addr,
		},

		mux: http.NewServeMux(),

		api:    api.NewApiGateway(cfg, logger),
		middle: middleware.NewMiddleware(cfg, logger),

		log: logger,
	}
}

func (s *Server) StartServer() {
	s.log.Info(fmt.Sprintf("starting _API_ server on %s", s.httpServer.Addr))

	s.httpServer.Handler = s.mux

	if err := s.httpServer.ListenAndServe(); err != nil {
		log.Fatal(errs.ErrCantStartServer(err))
	}

}

func (s *Server) GracefulStop(ctx context.Context) {
	s.api.CloseAuth()
	s.api.CloseChecker()

	s.httpServer.Shutdown(ctx)
}
