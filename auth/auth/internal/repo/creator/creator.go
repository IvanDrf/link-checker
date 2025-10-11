package creator

import (
	"context"
	"database/sql"
	"fmt"
	"log/slog"
	"time"
)

type TableCreator interface {
	CreateUsersTable() error
	CreateJWTTable() error
}

const (
	UsersTable = "users"
	JWTTable   = "tokens"
)

type tableCreator struct {
	db *sql.DB

	log *slog.Logger
}

const ctxTime = 5 * time.Second

func NewCreator(db *sql.DB, log *slog.Logger) TableCreator {
	return &tableCreator{
		db:  db,
		log: log,
	}
}

func (t *tableCreator) CreateUsersTable() error {
	query := fmt.Sprintf(`CREATE TABLE IF NOT EXISTS %s(
		user_id INTEGER PRIMARY KEY,
		email TINYTEXT NOT NULL UNIQUE,
		password TINYTEXT NOT NULL
	)`, UsersTable)

	ctx, cancel := context.WithTimeout(context.Background(), ctxTime)
	defer cancel()

	_, err := t.db.ExecContext(ctx, query)
	return err
}

func (t *tableCreator) CreateJWTTable() error {
	query := fmt.Sprintf(`CREATE TABLE IF NOT EXISTS %s(
		token_id INTEGER PRIMARY KEY,
		token TEXT NOT NULL,
		user_id INTEGER NOT NULL,

		FOREIGN KEY (user_id) REFERENCES TO users(user_id)
	)`, JWTTable)

	ctx, cancel := context.WithTimeout(context.Background(), ctxTime)
	defer cancel()

	_, err := t.db.ExecContext(ctx, query)
	return err
}
