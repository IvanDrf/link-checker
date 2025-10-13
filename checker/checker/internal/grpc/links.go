package links

import (
	"checker/checker/internal/config"
	linkService "checker/checker/internal/service/links"
	"checker/protos/gen-go/checkerv1"
	"context"
	"log/slog"

	"google.golang.org/grpc"
)

type serverAPI struct {
	linker linkService.Linker
	checkerv1.UnimplementedCheckerServer
}

func Register(gRPC *grpc.Server, cfg *config.Config, log *slog.Logger) {
	checkerv1.RegisterCheckerServer(gRPC, &serverAPI{
		linker: linkService.NewLinker(),
	})
}
func (s *serverAPI) CheckLinks(ctx context.Context, req *checkerv1.CheckRequest) (*checkerv1.CheckResponse, error) {
	return nil, nil
}
