package authService

import (
	"auth/auth/internal/models"
	"context"
	"database/sql"
	"log/slog"
)

const usersTable = "users"

type AuthService interface {
	Register(ctx context.Context, user *models.User) error
	//Login(ctx context.Context)
	//IsAdmin(ctx context.Context)
}

type authService struct {
	log *slog.Logger
}

func NewAuthService(db *sql.DB, log *slog.Logger) AuthService {
	return &authService{

		log: log,
	}
}

func (a *authService) Register(ctx context.Context, user *models.User) error {
	return nil
}
