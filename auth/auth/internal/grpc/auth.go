package auth

import (
	"auth/auth/internal/models"
	authService "auth/auth/internal/service/auth"
	"auth/protos/gen-go/authv1"
	"context"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

const (
	ctxTime = 5 * time.Second
)

type serverAPI struct {
	auther authService.AuthService
	authv1.UnimplementedAuthServer
}

func Register(gRPC *grpc.Server) {
	authv1.RegisterAuthServer(gRPC, &serverAPI{})
}

func (s *serverAPI) Register(ctx context.Context, req *authv1.RegisterRequest) (*authv1.RegisterResponse, error) {
	ctx, cancel := context.WithTimeout(context.Background(), ctxTime)
	defer cancel()

	user := models.User{Email: req.GetEmail(), Password: req.GetEmail()}
	if err := s.auther.Register(ctx, &user); err != nil {
		return nil, status.Error(codes.Canceled, err.Error())
	}

	return &authv1.RegisterResponse{
		UserId: user.Id,
	}, nil
}

func (s *serverAPI) Login(ctx context.Context, req *authv1.LoginRequest) (*authv1.LoginResponse, error) {
	return nil, nil
}
