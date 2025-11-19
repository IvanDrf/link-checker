package auth

import (
	"context"
	"database/sql"
	"errors"
	"log/slog"

	"github.com/IvanDrf/auth/internal/config"
	"github.com/IvanDrf/auth/internal/errs"
	"github.com/IvanDrf/auth/internal/models"
	"github.com/IvanDrf/auth/internal/service"
	authService "github.com/IvanDrf/auth/internal/service/auth"
	auth_api "github.com/IvanDrf/link-checker/pkg/auth-api"
	"github.com/redis/go-redis/v9"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type serverAPI struct {
	auther service.AuthService
	auth_api.UnimplementedAuthServer
}

func Register(gRPC *grpc.Server, cfg *config.Config, db *sql.DB, rdb *redis.Client, log *slog.Logger) {
	auth_api.RegisterAuthServer(gRPC, &serverAPI{
		auther: authService.NewAuthService(cfg, db, rdb, log),
	})
}

func (s *serverAPI) Register(ctx context.Context, req *auth_api.RegisterRequest) (*auth_api.RegisterResponse, error) {
	user := &models.User{
		Email:    req.GetEmail(),
		Password: req.GetPassword(),
	}

	var err error
	var verifToken string

	user, verifToken, err = s.auther.Register(ctx, user)
	if errors.Is(err, errs.ErrInvalidEmail()) {
		return nil, status.Error(codes.InvalidArgument, err.Error())
	}

	if errors.Is(err, errs.ErrUserAlreadyInDB()) {
		return nil, status.Error(codes.Canceled, err.Error())
	}

	if errors.Is(err, errs.ErrCantAddNewUser()) {
		return nil, status.Error(codes.Internal, err.Error())
	}

	if errors.Is(err, errs.ErrCantCreateVerifToken()) {
		return nil, status.Error(codes.Internal, err.Error())
	}

	if errors.Is(err, errs.ErrCantSaveVerifToken()) {
		return nil, status.Error(codes.Internal, err.Error())
	}

	return &auth_api.RegisterResponse{
		UserId:     user.Id,
		VerifToken: verifToken,
	}, nil
}

func (s *serverAPI) Login(ctx context.Context, req *auth_api.LoginRequest) (*auth_api.LoginResponse, error) {
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

	return &auth_api.LoginResponse{
		Access:  access,
		Refresh: refresh,
	}, nil

}

func (s *serverAPI) RefreshTokens(ctx context.Context, req *auth_api.RefreshRequest) (*auth_api.RefreshResponse, error) {
	access, refresh, err := s.auther.RefreshTokens(ctx, req.GetRefresh())
	if err != nil {
		return nil, status.Error(codes.InvalidArgument, err.Error())
	}

	return &auth_api.RefreshResponse{
		Access:  access,
		Refresh: refresh,
	}, nil
}
