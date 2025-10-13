package authService

import (
	"auth/auth/internal/errs"
	"auth/auth/internal/models"
	userRepo "auth/auth/internal/repo/user"
	"auth/auth/pkg/email"
	"auth/auth/pkg/hasher"
	"context"
	"database/sql"
	"log/slog"
)

type AuthService interface {
	Register(ctx context.Context, user *models.User) (*models.User, error)
	//Login(ctx context.Context)
	//IsAdmin(ctx context.Context)
}

type authService struct {
	users userRepo.UserRepo

	hasher         hasher.PswHasher
	emailValidator email.EmailValidator

	log *slog.Logger
}

func NewAuthService(db *sql.DB, log *slog.Logger) AuthService {
	return &authService{
		users: userRepo.NewRepo(db, log),

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
