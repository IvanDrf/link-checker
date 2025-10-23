package main

import (
	"auth/auth/internal/repo"
	"errors"
	"flag"
	"fmt"
	"log"

	"github.com/golang-migrate/migrate/v4"
	_ "github.com/golang-migrate/migrate/v4/database/sqlite3"
	_ "github.com/golang-migrate/migrate/v4/source/file"
)

func main() {
	storagePath, migrationsPath := "", ""

	flag.StringVar(&storagePath, "storage-path", "", "path to database(storage)")
	flag.StringVar(&migrationsPath, "migrations-path", "", "path to migrations")

	flag.Parse()
	checkPaths(storagePath, migrationsPath)

	m, err := migrate.New("file://"+migrationsPath, fmt.Sprintf("sqlite3://%s?x-migrations-table=%s", storagePath, repo.UsersTable))
	if err != nil {
		log.Fatal(err)
	}

	err = m.Up()
	if err != nil {
		if errors.Is(err, migrate.ErrNoChange) {
			log.Println("no migrations")
			return
		}

		log.Fatal(err)
	}

	log.Println("migrations applied")
}

func checkPaths(storagePath, migrationsPath string) {
	if storagePath == "" {
		log.Fatal("storage path is empty")
	}

	if migrationsPath == "" {
		log.Fatal("migrations path is empty")
	}
}
