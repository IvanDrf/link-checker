package links

import (
	"checker/checker/internal/config"
	"checker/checker/internal/errs"
	"checker/checker/internal/service"
	linkService "checker/checker/internal/service/links"
	"checker/protos/gen-go/checkerv1"
	"context"
	"fmt"
	"log/slog"
	"time"

	"github.com/redis/go-redis/v9"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

const (
	maxLinksCount = 150
	timeFormat    = "15:05:04:05"
)

type serverAPI struct {
	linkChecker service.LinkChecker

	log *slog.Logger
	checkerv1.UnimplementedCheckerServer
}

func Register(gRPC *grpc.Server, cfg *config.Config, rdb *redis.Client, logger *slog.Logger) {
	checkerv1.RegisterCheckerServer(gRPC, &serverAPI{
		linkChecker: linkService.NewLinkChecker(rdb, logger),
		log:         logger,
	})
}

func (s *serverAPI) CheckLinks(ctx context.Context, req *checkerv1.CheckRequest) (*checkerv1.CheckResponse, error) {
	s.log.Info(fmt.Sprintf("CheckLinks -> get request: %s", time.Now().Format(timeFormat)))

	if len(req.Links) >= maxLinksCount {
		s.log.Info(fmt.Sprintf("CheckLinks -> too many links: %v", len(req.Links)))

		return nil, status.Error(codes.OutOfRange, errs.ErrTooManyLinksInRequest().Error())
	}

	links := s.linkChecker.CheckLinks(ctx, req.Links)

	resp := &checkerv1.CheckResponse{
		Links: make([]*checkerv1.Link, 0, len(links)),
	}

	for i := range links {
		resp.Links = append(resp.Links, &checkerv1.Link{
			Link:   links[i].Link,
			Status: links[i].Status,
		})
	}

	s.log.Info(fmt.Sprintf("CheckLinks -> send response:, %s", time.Now().Format(timeFormat)))

	return resp, nil
}
