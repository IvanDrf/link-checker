package links

import (
	"checker/checker/internal/config"
	"checker/checker/internal/errs"
	urlService "checker/checker/internal/service/url"
	"checker/protos/gen-go/checkerv1"
	"context"
	"log/slog"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type serverAPI struct {
	urlChecker urlService.UrlChecker
	checkerv1.UnimplementedCheckerServer
}

func Register(gRPC *grpc.Server, cfg *config.Config, log *slog.Logger) {
	checkerv1.RegisterCheckerServer(gRPC, &serverAPI{
		urlChecker: urlService.NewUrlChecker(),
	})
}

func (s *serverAPI) CheckLinks(ctx context.Context, req *checkerv1.CheckRequest) (*checkerv1.CheckResponse, error) {
	if len(req.Urls) >= 150 {
		return nil, status.Error(codes.OutOfRange, errs.ErrTooManyUrls().Error())
	}

	urls := s.urlChecker.CheckUrls(ctx, req.Urls)

	resp := &checkerv1.CheckResponse{
		Urls: make([]*checkerv1.Url, 0, len(urls)),
	}

	for i := range urls {
		resp.Urls = append(resp.Urls, &checkerv1.Url{
			Url:    urls[i].Url,
			Status: urls[i].Status,
		})
	}

	return resp, nil
}
