package authService

import (
	"context"
	"database/sql"
	"github.com/IvanDrf/auth/internal/config"
	"github.com/IvanDrf/auth/internal/errs"
	"github.com/IvanDrf/auth/internal/lib/jwter"
	"github.com/IvanDrf/auth/internal/models"
	userRepo "github.com/IvanDrf/auth/internal/repo/user"
	"github.com/IvanDrf/auth/pkg/email"
	"github.com/IvanDrf/auth/pkg/hasher"
	"log/slog"
)

type AuthService interface {
	Register(ctx context.Context, user *models.User) (*models.User, error)
	Login(ctx context.Context, user *models.User) (string, string, error)
	RefreshTokens(ctx context.Context, refreshToken string) (string, string, error)
}

type authService struct {
	users userRepo.UserRepo

	jwter          jwter.JWTer
	hasher         hasher.PswHasher
	emailValidator email.EmailValidator

	log *slog.Logger
}

func NewAuthService(cfg *config.Config, db *sql.DB, log *slog.Logger) AuthService {
	return &authService{
		users: userRepo.NewRepo(db, log),

		jwter:          jwter.NewJWTer(cfg),
		hasher:         hasher.NewPswHasher(),
		emailValidator: email.NewValidator(),

		log: log,
	}
}

func (a *authService) Register(ctx context.Context, user *models.User) (*models.User, error) {
	a.log.Info("Register request")

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
