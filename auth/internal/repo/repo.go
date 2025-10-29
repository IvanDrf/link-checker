package repo

import (
	"context"

	"github.com/IvanDrf/auth/internal/models"
)

type UserRepo interface {
	AddUser(ctx context.Context, user *models.User) (int64, error)
	FindUserByEmail(ctx context.Context, email string) (*models.User, error)
}
