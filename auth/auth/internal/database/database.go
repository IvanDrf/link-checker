package database

import (
	"auth/auth/internal/config"
	"auth/auth/internal/repo/creator"
	"context"
	"database/sql"
	"log"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

func InitDatabase(cfg *config.Config) *sql.DB {
	db, err := sql.Open("sqlite3", cfg.StoragePath)

	if err != nil {
		log.Fatal(err)
	}

	createNecessaryTables(db)

	return db
}

const ctxTime = 5 * time.Second

func createNecessaryTables(db *sql.DB) {
	tableCreator := creator.NewCreator(db)

	ctx, cancel := context.WithTimeout(context.Background(), ctxTime)
	defer cancel()

	if err := tableCreator.CreateUsersTable(ctx); err != nil {
		log.Fatal(err)
	}

	if err := tableCreator.CreateJWTTable(ctx); err != nil {
		log.Fatal(err)
	}
}
