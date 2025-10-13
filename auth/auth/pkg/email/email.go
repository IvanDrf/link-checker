package email

import "regexp"

type EmailValidator interface {
	IsEmailValid(email string) bool
}

type emailValidator struct {
}

func NewValidator() EmailValidator {
	return &emailValidator{}
}

const re = `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

func (e *emailValidator) IsEmailValid(email string) bool {
	return regexp.MustCompile(re).MatchString(email)
}
