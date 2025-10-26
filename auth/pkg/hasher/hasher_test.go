package hasher

import (
	"sync"
	"testing"

	"github.com/stretchr/testify/assert"
)

var passwords = []string{
	"123",
	"stRong_Password1L",
	"6Wqwerty",
}

func TestPasswordHashing(t *testing.T) {
	hasher := NewPswHasher()

	wg := new(sync.WaitGroup)
	wg.Add(len(passwords))

	for _, password := range passwords {
		go func(password string) {
			defer wg.Done()
			assert.NotEqual(t, password, hasher.HashPassword(password))
		}(password)
	}

	wg.Wait()
}

func TestPaswordComparing(t *testing.T) {
	hashedPasswords := make([]string, len(passwords))

	hasher := NewPswHasher()

	wg := new(sync.WaitGroup)
	wg.Add(len(passwords))

	for i, password := range passwords {
		go func(i int, password string) {
			defer wg.Done()
			hashedPasswords[i] = hasher.HashPassword(password)
		}(i, password)
	}

	wg.Wait()

	for i := range passwords {
		assert.Equal(t, true, hasher.ComparePassword(hashedPasswords[i], passwords[i]))
	}
}
