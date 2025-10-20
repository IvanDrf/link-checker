package jwt

import (
	"api-gateway/internal/config"
	"api-gateway/internal/errs"
	"net/http"

	"github.com/golang-jwt/jwt"
)

type JWTer interface {
	GetToken(tokenType string, r *http.Request) (string, error)

	IsValid(tokenStr string) error
}

type jwter struct {
	jwtSecret []byte
}

func NewJWTer(cfg *config.Config) JWTer {
	return &jwter{
		jwtSecret: []byte(cfg.Auth.JWT.Key),
	}
}

const (
	AccessToken  = "access_jwt"
	RefreshToken = "refresh_jwt"
)

func (j *jwter) GetToken(tokenType string, r *http.Request) (string, error) {
	if tokenType != AccessToken && tokenType != RefreshToken {
		return "", errs.ErrInvalidTokenTypeCookies()
	}

	cookie, err := r.Cookie(tokenType)
	if err != nil {
		return "", errs.ErrCantFindTokenCookies()
	}

	return cookie.Value, nil
}

func (j *jwter) IsValid(tokenStr string) error {
	token, err := jwt.Parse(tokenStr, func(t *jwt.Token) (interface{}, error) {
		if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, errs.ErrInvalidJWTMethod()
		}

		return j.jwtSecret, nil
	})

	if err != nil {
		return err
	}

	if !token.Valid {
		return errs.ErrInvalidJWTToken()
	}

	return nil
}
