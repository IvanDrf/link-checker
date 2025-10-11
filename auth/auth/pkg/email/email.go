package email

import "regexp"

type EmailValidater interface {
	IsEmailValid(email string) bool
}

type emailValidater struct {
}

func New() EmailValidater {
	return &emailValidater{}
}

const re = `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

func (e *emailValidater) IsEmailValid(email string) bool {
	return regexp.MustCompile(re).MatchString(email)
}
