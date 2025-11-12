package authService

import (
	"context"
	"database/sql"
	"log/slog"

	"github.com/IvanDrf/auth/internal/config"
	"github.com/IvanDrf/auth/internal/errs"
	"github.com/IvanDrf/auth/internal/lib/jwter"
	"github.com/IvanDrf/auth/internal/models"
	"github.com/IvanDrf/auth/internal/repo"
	userRepo "github.com/IvanDrf/auth/internal/repo/user"
	"github.com/IvanDrf/auth/internal/service"
	"github.com/IvanDrf/auth/pkg/email"
	"github.com/IvanDrf/auth/pkg/hasher"
)

type authService struct {
	users repo.UserRepo

	jwter          jwter.JWTer
	hasher         hasher.PswHasher
	emailValidator email.EmailValidator

	logger *slog.Logger
}

func NewAuthService(cfg *config.Config, db *sql.DB, logger *slog.Logger) service.AuthService {
	return &authService{
		users: userRepo.NewRepo(db),

		jwter:          jwter.NewJWTer(cfg),
		hasher:         hasher.NewPswHasher(),
		emailValidator: email.NewValidator(),

		logger: logger,
	}
}

func (a *authService) Register(ctx context.Context, user *models.User) (*models.User, error) {
	a.logger.Info("Register request")

	if !a.emailValidator.IsEmailValid(user.Email) {
		return nil, errs.ErrInvalidEmail()
	}

	_, err := a.users.FindUserByEmail(ctx, user.Email)
	if err == nil {
		return nil, errs.ErrUserAlreadyInDB()
	}

	user.Password = a.hasher.HashPassword(user.Password)

	user.Id, err = a.users.AddUser(ctx, user)
	if err != nil {
		return nil, errs.ErrCantAddNewUser()
	}

	return user, nil
}

func (a *authService) Login(ctx context.Context, user *models.User) (string, string, error) {
	a.logger.Info("Login request")
	userInDB, err := a.users.FindUserByEmail(ctx, user.Email)
	if err != nil {
		return "", "", errs.ErrCantFindUserInDB()
	}

	if !a.hasher.ComparePassword(userInDB.Password, user.Password) {
		return "", "", errs.ErrIncorrectPassword()
	}

	access, refresh, err := a.jwter.GenerateTokens(userInDB.Id)
	if err != nil {
		return "", "", errs.ErrCantCreateJWT()
	}

	return access, refresh, nil
}

func (a *authService) RefreshTokens(ctx context.Context, refreshToken string) (string, string, error) {
	return a.jwter.RefreshTokens(refreshToken)
}
