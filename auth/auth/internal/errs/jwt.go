package errs

import (
	"net/http"
)

func ErrCantCreateJWT() error {
	return Error{Code: http.StatusInternalServerError, Msg: "cant create jwt token"}
}

func ErrIncorrectJWT() error {
	return Error{Code: http.StatusBadRequest, Msg: "jwt token is incorrect"}
}
