#!/bin/bash

build_checker() { 
    cd ./checker
    go build -o checker cmd/main.go 
}

build_auth() {
    cd ./auth
    go build -o auth cmd/app/main.go 
}

build_api() {
    cd ./api
    go build -o api cmd/main.go
}

build_checker
cd  ..

build_auth
cd  ..

build_api
cd  ..