package service

import (
	"context"

	"github.com/IvanDrf/auth/internal/models"
)

type AuthService interface {
	Register(ctx context.Context, user *models.User) (*models.User, string, error)
	VerifyEmail(ctx context.Context, link string) error
	Login(ctx context.Context, user *models.User) (string, string, error)

	RefreshTokens(ctx context.Context, refreshToken string) (string, string, error)
}
