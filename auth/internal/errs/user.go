package errs

func ErrUserAlreadyInDB() error {
	return Error{Msg: "user with that email already exists"}
}

func ErrInvalidEmail() error {
	return Error{Msg: "invalid email in request"}
}

func ErrCantAddNewUser() error {
	return Error{Msg: "cant add new user in database"}
}

func ErrCantFindUserInDB() error {
	return Error{Msg: "cant find user in database"}
}

func ErrIncorrectPassword() error {
	return Error{Msg: "password is incorrect"}
}

func ErrCantVerificateUser(email string) error {
	return Error{Msg: "cant verificate user with email: %s"}
}

func ErrEmailIsNotVerificated() error {
	return Error{Msg: "user with this email is not verificated"}
}
