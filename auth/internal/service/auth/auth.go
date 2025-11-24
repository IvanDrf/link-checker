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
	tokenRepo "github.com/IvanDrf/auth/internal/repo/token"
	userRepo "github.com/IvanDrf/auth/internal/repo/user"
	"github.com/IvanDrf/auth/internal/service"
	"github.com/IvanDrf/auth/pkg/email"
	"github.com/IvanDrf/auth/pkg/hasher"
	"github.com/IvanDrf/auth/pkg/token"
	"github.com/redis/go-redis/v9"
)

type authService struct {
	users repo.UserRepo
	links repo.TokenRepo

	jwter jwter.JWTer

	hasher         hasher.PswHasher
	emailValidator email.EmailValidator
	tokenCreator   token.VerifTokenCreator

	logger *slog.Logger
}

func NewAuthService(cfg *config.Config, db *sql.DB, rdb *redis.Client, logger *slog.Logger) service.AuthService {
	return &authService{
		users: userRepo.NewRepo(db),
		links: tokenRepo.NewTokenRepo(rdb),

		jwter: jwter.NewJWTer(cfg),

		hasher:         hasher.NewPswHasher(),
		emailValidator: email.NewValidator(),
		tokenCreator:   token.NewVerifTokenCreator(),

		logger: logger,
	}
}

func (a *authService) Register(ctx context.Context, user *models.User) (*models.User, string, error) {
	a.logger.Info("Register request")

	if !a.emailValidator.IsEmailValid(user.Email) {
		return nil, "", errs.ErrInvalidEmail()
	}

	_, err := a.users.FindUserByEmail(ctx, user.Email)
	if err == nil {
		return nil, "", errs.ErrUserAlreadyInDB()
	}

	user.Password = a.hasher.HashPassword(user.Password)

	user.Id, err = a.users.AddUser(ctx, user)
	if err != nil {
		return nil, "", errs.ErrCantAddNewUser()
	}

	verifToken := a.tokenCreator.CreateVerifToken()
	if verifToken == "" {
		return nil, "", errs.ErrCantCreateVerifToken()
	}

	err = a.links.AddToken(ctx, verifToken, user.Email)
	if err != nil {
		return nil, "", errs.ErrCantSaveVerifToken()
	}

	return user, verifToken, nil
}

func (a *authService) VerifyEmail(ctx context.Context, link string) error {
	email, err := a.links.GetEmailByToken(ctx, link)
	if err != nil {
		return err
	}

	err = a.users.UpdateUserVerification(ctx, email)
	if err != nil {
		return errs.ErrCantVerificateUser(email)
	}

	return nil
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

	if !userInDB.Verificated {
		return "", "", errs.ErrEmailIsNotVerificated()
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
