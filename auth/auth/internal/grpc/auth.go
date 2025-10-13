package auth

import (
	"auth/auth/internal/models"
	authService "auth/auth/internal/service/auth"
	"auth/protos/gen-go/authv1"
	"context"
	"database/sql"
	"log/slog"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type serverAPI struct {
	auther authService.AuthService
	authv1.UnimplementedAuthServer
}

func Register(gRPC *grpc.Server, db *sql.DB, log *slog.Logger) {
	authv1.RegisterAuthServer(gRPC, &serverAPI{
		auther: authService.NewAuthService(db, log),
	})
}

func (s *serverAPI) Register(ctx context.Context, req *authv1.RegisterRequest) (*authv1.RegisterResponse, error) {
	user := &models.User{
		Email:    req.GetEmail(),
		Password: req.GetEmail(),
	}

	var err error
	user, err = s.auther.Register(ctx, user)
	if err != nil {
		return nil, status.Error(codes.Canceled, err.Error())
	}

	return &authv1.RegisterResponse{
		UserId: user.Id,
	}, nil
}

func (s *serverAPI) Login(ctx context.Context, req *authv1.LoginRequest) (*authv1.LoginResponse, error) {
	return nil, nil
}
