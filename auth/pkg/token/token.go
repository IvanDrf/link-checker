package token

import (
	"crypto/rand"
	"encoding/hex"
)

type VerifTokenCreator interface {
	CreateVerifToken() string
}

type tokenCreator struct {
}

func NewVerifTokenCreator() VerifTokenCreator {
	return &tokenCreator{}
}

func (l *tokenCreator) CreateVerifToken() string {
	buff := make([]byte, 32)

	if _, err := rand.Read(buff); err != nil {
		return ""
	}

	token := hex.EncodeToString(buff)
	return token

}
