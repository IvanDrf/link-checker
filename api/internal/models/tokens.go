package models

type Tokens struct {
	Access  string `json:"access_jwt" validate:"required,access_jwt"`
	Refresh string `json:"refresh_jwt" validate:"required,refresh_jwt"`
}
