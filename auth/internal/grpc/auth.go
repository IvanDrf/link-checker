package auth

import (
	"auth/protos/gen-go/authv1"
	"context"
	"database/sql"
	"errors"
	"github.com/IvanDrf/auth/internal/config"
	"github.com/IvanDrf/auth/internal/errs"
	"github.com/IvanDrf/auth/internal/models"
	authService "github.com/IvanDrf/auth/internal/service/auth"
	"log/slog"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type serverAPI struct {
	auther authService.AuthService
	authv1.UnimplementedAuthServer
}

func Register(gRPC *grpc.Server, cfg *config.Config, db *sql.DB, log *slog.Logger) {
	authv1.RegisterAuthServer(gRPC, &serverAPI{
		auther: authService.NewAuthService(cfg, db, log),
	})
}

func (s *serverAPI) Register(ctx context.Context, req *authv1.RegisterRequest) (*authv1.RegisterResponse, error) {
	user := &models.User{
		Email:    req.GetEmail(),
		Password: req.GetPassword(),
	}

	var err error
	user, err = s.auther.Register(ctx, user)
	if errors.Is(err, errs.ErrInvalidEmail()) {
		return nil, status.Error(codes.InvalidArgument, err.Error())
	}

	if errors.Is(err, errs.ErrUserAlreadyInDB()) {
		return nil, status.Error(codes.Canceled, err.Error())
	}

	if errors.Is(err, errs.ErrCantAddNewUser()) {
		return nil, status.Error(codes.Internal, err.Error())
	}

	return &authv1.RegisterResponse{
		UserId: user.Id,
	}, nil
}

func (s *serverAPI) Login(ctx context.Context, req *authv1.LoginRequest) (*authv1.LoginResponse, error) {
	user := &models.User{
		Email:    req.GetEmail(),
		Password: req.GetPassword(),
	}

	access, refresh, err := s.auther.Login(ctx, user)
	if errors.Is(err, errs.ErrCantFindUserInDB()) {
		return nil, status.Error(codes.Unauthenticated, err.Error())
	}

	if errors.Is(err, errs.ErrIncorrectPassword()) {
		return nil, status.Error(codes.InvalidArgument, err.Error())
	}

	if errors.Is(err, errs.ErrCantCreateJWT()) {
		return nil, status.Error(codes.Internal, err.Error())
	}

	return &authv1.LoginResponse{
		Access:  access,
		Refresh: refresh,
	}, nil

}

func (s *serverAPI) RefreshTokens(ctx context.Context, req *authv1.RefreshRequest) (*authv1.RefreshResponse, error) {
	access, refresh, err := s.auther.RefreshTokens(ctx, req.GetRefresh())
	if err != nil {
		return nil, status.Error(codes.InvalidArgument, err.Error())
	}

	return &authv1.RefreshResponse{
		Access:  access,
		Refresh: refresh,
	}, nil
}
