package jwter

import (
	"auth/auth/internal/config"
	"auth/auth/internal/errs"

	"time"

	"github.com/golang-jwt/jwt"
)

type JWTer interface {
	GenerateTokens(userID int64) (string, string, error)
	RefreshTokens(refreshToken string) (string, string, error)
}

type jwter struct {
	jwtSecret []byte

	accessExpTime  time.Duration
	refreshExpTime time.Duration
}

func NewJWTer(cfg *config.Config) JWTer {
	return &jwter{
		jwtSecret:      []byte(cfg.JWT.Key),
		accessExpTime:  cfg.JWT.AccessExpTime,
		refreshExpTime: cfg.JWT.RefreshExpTime,
	}
}

func (j *jwter) GenerateTokens(userID int64) (string, string, error) {
	access, err := j.generateToken(userID, j.accessExpTime)
	if err != nil {
		return "", "", errs.ErrCantCreateJWT()
	}

	refresh, err := j.generateToken(userID, j.refreshExpTime)
	if err != nil {
		return "", "", errs.ErrCantCreateJWT()
	}

	return access, refresh, nil
}

func (j *jwter) generateToken(userID int64, duration time.Duration) (string, error) {
	token := jwt.New(jwt.SigningMethodHS256)

	claims := token.Claims.(jwt.MapClaims)
	claims["uid"] = userID
	claims["exp"] = time.Now().Add(duration).Unix()

	tokenString, err := token.SignedString(j.jwtSecret)
	if err != nil {
		return "", err
	}

	return tokenString, nil
}

func (j *jwter) RefreshTokens(refreshToken string) (string, string, error) {
	claims, err := j.getClaims(refreshToken)
	if err != nil {
		return "", "", err
	}

	floatID, ok := claims["uid"].(float64)
	if !ok {
		return "", "", errs.ErrIncorrectJWT()
	}

	userID := int64(floatID)

	return j.GenerateTokens(userID)
}

func (j *jwter) getClaims(refreshToken string) (jwt.MapClaims, error) {
	token, err := jwt.ParseWithClaims(refreshToken, jwt.MapClaims{}, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, errs.ErrIncorrectJWT()
		}

		return j.jwtSecret, nil
	})

	if err != nil {
		return nil, err
	}

	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		return claims, nil
	}

	return nil, errs.ErrIncorrectJWT()
}
