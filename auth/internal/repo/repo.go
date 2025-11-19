package repo

import (
	"context"

	"github.com/IvanDrf/auth/internal/models"
)

type UserRepo interface {
	AddUser(ctx context.Context, user *models.User) (int64, error)
	FindUserByEmail(ctx context.Context, email string) (*models.User, error)

	UpdateUserVerification(ctx context.Context, email string) error
}

// Repo for verification email tokens, not jwt
type TokenRepo interface {
	AddToken(ctx context.Context, token string, email string) error
	GetEmailByToken(ctx context.Context, token string) (string, error)
}
