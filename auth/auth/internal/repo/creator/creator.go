package creator

import (
	"context"
	"database/sql"
	"fmt"
)

type TableCreator interface {
	CreateUsersTable(ctx context.Context) error
	CreateJWTTable(ctx context.Context) error
}

const (
	UsersTable = "users"
	JWTTable   = "tokens"
)

type tableCreator struct {
	db *sql.DB
}

func NewCreator(db *sql.DB) TableCreator {
	return &tableCreator{
		db: db,
	}
}

func (t *tableCreator) CreateUsersTable(ctx context.Context) error {
	query := fmt.Sprintf(`CREATE TABLE IF NOT EXISTS %s(
		user_id INTEGER PRIMARY KEY,
		email TINYTEXT NOT NULL UNIQUE,
		password TEXT NOT NULL
	)`, UsersTable)

	_, err := t.db.ExecContext(ctx, query)
	return err
}

func (t *tableCreator) CreateJWTTable(ctx context.Context) error {
	query := fmt.Sprintf(`CREATE TABLE IF NOT EXISTS %s(
		token_id INTEGER PRIMARY KEY,
		token TEXT NOT NULL,
		user_id INTEGER NOT NULL,

		FOREIGN KEY (user_id) REFERENCES users(user_id)
	)`, JWTTable)

	_, err := t.db.ExecContext(ctx, query)
	return err
}
