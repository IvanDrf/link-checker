package userRepo

import (
	"context"
	"database/sql"
	"fmt"
	"github.com/IvanDrf/auth/internal/models"
	"github.com/IvanDrf/auth/internal/repo"
	"log/slog"
)

type UserRepo interface {
	AddUser(ctx context.Context, user *models.User) (int64, error)
	FindUserByEmail(ctx context.Context, email string) (*models.User, error)
}

type userRepo struct {
	db *sql.DB

	log *slog.Logger
}

func NewRepo(db *sql.DB, log *slog.Logger) UserRepo {
	return &userRepo{
		db:  db,
		log: log,
	}
}

func (r *userRepo) AddUser(ctx context.Context, user *models.User) (int64, error) {
	query := fmt.Sprintf("INSERT INTO %s (email, password) VALUES(?, ?)", repo.UsersTable)

	res, err := r.db.ExecContext(ctx, query, user.Email, user.Password)
	if err != nil {
		return -1, err
	}

	return res.LastInsertId()
}

func (r *userRepo) FindUserByEmail(ctx context.Context, email string) (*models.User, error) {
	query := fmt.Sprintf("SELECT user_id, email, password FROM %s WHERE email = ?", repo.UsersTable)

	user := models.User{}
	err := r.db.QueryRowContext(ctx, query, email).Scan(&user.Id, &user.Email, &user.Password)
	if err != nil {
		return nil, err
	}

	return &user, nil
}
