package cookies

import (
	"net/http"

	"github.com/IvanDrf/api-gateway/internal/transport/jwt"
)

type Cookier interface {
	SetAuthCookies(w http.ResponseWriter, access, refresh string)
}

type cookier struct {
}

func NewCookier() Cookier {
	return &cookier{}
}

func (c *cookier) SetAuthCookies(w http.ResponseWriter, access, refresh string) {
	http.SetCookie(w, &http.Cookie{
		Name:     jwt.AccessToken,
		Value:    access,
		Path:     "/",
		Secure:   true,
		HttpOnly: true,
		SameSite: http.SameSiteLaxMode,
	})

	http.SetCookie(w, &http.Cookie{
		Name:     jwt.RefreshToken,
		Value:    refresh,
		Path:     "/",
		Secure:   true,
		HttpOnly: true,
		SameSite: http.SameSiteLaxMode,
	})
}
