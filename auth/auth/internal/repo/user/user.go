package userRepo

import (
	"auth/auth/internal/models"
	"auth/auth/internal/repo/creator"
	"context"
	"database/sql"
	"fmt"
	"log/slog"
)

type UserRepo interface {
	AddUser(ctx context.Context, user *models.User) (int64, error)
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
	res, err := r.db.ExecContext(ctx, fmt.Sprintf("INSERT INTO %s (email, password) VALUES(?, ?)", creator.UsersTable))
	if err != nil {
		return -1, err
	}

	return res.LastInsertId()
}
