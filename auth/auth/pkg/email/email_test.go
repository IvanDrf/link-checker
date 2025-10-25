package email

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestValidEmails(t *testing.T) {
	validEmails := []string{
		"ivan@gmail.com",
		"example@mail.com",
		"ivan@yandex.ru",
	}

	testValidator(t, validEmails, true)
}

func TestInvalidEmails(t *testing.T) {
	invalidEmails := []string{
		"1",
		"example.com",
		"",
		"@",
	}

	testValidator(t, invalidEmails, false)
}

func testValidator(t *testing.T, emails []string, expected bool) {
	validator := NewValidator()

	for _, email := range emails {
		assert.Equal(t, expected, validator.IsEmailValid(email))
	}
}
