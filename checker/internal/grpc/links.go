package links

import (
	"context"
	"fmt"
	"log/slog"
	"time"

	checker_api "github.com/IvanDrf/link-checker/pkg/checker-api"

	"github.com/IvanDrf/checker/internal/config"
	"github.com/IvanDrf/checker/internal/errs"
	"github.com/IvanDrf/checker/internal/service"
	linkService "github.com/IvanDrf/checker/internal/service/links"

	"github.com/redis/go-redis/v9"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

const (
	timeFormat = "15:05:04:05"
)

type serverAPI struct {
	linkChecker service.LinkChecker

	logger *slog.Logger
	checker_api.UnimplementedCheckerServer
}

func Register(gRPC *grpc.Server, cfg *config.Config, rdb *redis.Client, logger *slog.Logger) {
	checker_api.RegisterCheckerServer(gRPC, &serverAPI{
		linkChecker: linkService.NewLinkChecker(rdb, logger),
		logger:      logger,
	})
}

func (s *serverAPI) CheckLinks(ctx context.Context, req *checker_api.CheckRequest) (*checker_api.CheckResponse, error) {
	s.logger.Info(fmt.Sprintf("CheckLinks -> get request: %s", time.Now().Format(timeFormat)))

	if len(req.Links) > service.MaxLinksCount {
		s.logger.Info(fmt.Sprintf("CheckLinks -> too many links: %v", len(req.Links)))

		return nil, status.Error(codes.OutOfRange, errs.ErrTooManyLinksInRequest().Error())
	}

	links := s.linkChecker.CheckLinks(ctx, req.Links)

	resp := &checker_api.CheckResponse{
		Links: make([]*checker_api.Link, 0, len(links)),
	}

	for i := range links {
		resp.Links = append(resp.Links, &checker_api.Link{
			Link:   links[i].Link,
			Status: links[i].Status,
		})
	}

	s.logger.Info(fmt.Sprintf("CheckLinks -> send response:, %s", time.Now().Format(timeFormat)))

	return resp, nil
}
