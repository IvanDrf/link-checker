package errs

import "net/http"

func ErrInvalidTokenTypeCookies() error {
	return Error{
		Code: http.StatusUnauthorized,
		Msg:  "invalid token type in cookies, want: access/refresh",
	}
}

func ErrCantFindTokenCookies() error {
	return Error{
		Code: http.StatusUnauthorized,
		Msg:  "cant find access/refresh token in cookies",
	}
}

func ErrInvalidJWTMethod() error {
	return Error{
		Code: http.StatusUnauthorized,
		Msg:  "given invalid jwt token",
	}
}

func ErrInvalidJWTToken() error {
	return Error{
		Code: http.StatusUnauthorized,
		Msg:  "given invalid or expired token",
	}
}
