package database

import (
	"database/sql"
	"log"

	"github.com/IvanDrf/auth/internal/config"

	_ "github.com/mattn/go-sqlite3"
)

func InitDatabase(cfg *config.Config) *sql.DB {
	db, err := sql.Open("sqlite3", cfg.StoragePath)

	if err != nil {
		log.Fatal(err)
	}

	err = db.Ping()
	if err != nil {
		log.Fatal(err)
	}

	return db
}
