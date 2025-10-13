package hasher

import "golang.org/x/crypto/bcrypt"

type PswHasher interface {
	HashPassword(passw string) string
	ComparePassword(hashed, passw string) bool
}

type hasher struct {
}

func NewPswHasher() PswHasher {
	return hasher{}
}

const hashLen = 10

func (h hasher) HashPassword(passw string) string {
	bytes, _ := bcrypt.GenerateFromPassword([]byte(passw), hashLen)
	return string(bytes)
}

func (h hasher) ComparePassword(hashed, passw string) bool {
	return bcrypt.CompareHashAndPassword([]byte(hashed), []byte(passw)) == nil
}
