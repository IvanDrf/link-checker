package server

import (
	"context"
	"fmt"
	"log"
	"log/slog"
	"net/http"

	"github.com/IvanDrf/api-gateway/internal/config"
	"github.com/IvanDrf/api-gateway/internal/errs"
	"github.com/IvanDrf/api-gateway/internal/transport/api"
	"github.com/IvanDrf/api-gateway/internal/transport/middleware"
)

type Server struct {
	httpServer *http.Server
	mux        *http.ServeMux

	api    api.ApiGateway
	middle middleware.Middleware

	logger *slog.Logger
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

		logger: logger,
	}
}

func (s *Server) StartServer() {
	s.logger.Info(fmt.Sprintf("starting _API_ server on %s", s.httpServer.Addr))

	s.httpServer.Handler = s.mux

	if err := s.httpServer.ListenAndServe(); err != http.ErrServerClosed {
		log.Fatal(errs.ErrCantStartServer(err))
	}

}

func (s *Server) GracefulStop(ctx context.Context) {
	s.api.CloseAuth()
	s.api.CloseChecker()

	s.httpServer.Shutdown(ctx)
}
