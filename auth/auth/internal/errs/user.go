package errs

import "net/http"

func ErrUserAlreadyInDB() error {
	return Error{Code: http.StatusBadRequest, Msg: "user with that email already exists"}
}

func ErrInvalidEmail() error {
	return Error{Code: http.StatusBadRequest, Msg: "invalid email in request"}
}

func ErrCantAddNewUser() error {
	return Error{Code: http.StatusInternalServerError, Msg: "cant add new user in database"}
}

func ErrCantFindUserInDB() error {
	return Error{Code: http.StatusNotFound, Msg: "cant find user in database"}
}

func ErrIncorrectPassword() error {
	return Error{Code: http.StatusForbidden, Msg: "password is incorrect"}
}
