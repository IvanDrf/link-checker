package models

type Links struct {
	Links []string `json:"links" validate:"require links"`
}

type Link struct {
	Link   string `json:"link"`
	Status bool   `json:"status"`
}
