package errs

func ErrCantCreateJWT() error {
	return Error{Msg: "cant create jwt token"}
}

func ErrIncorrectJWT() error {
	return Error{Msg: "jwt token is incorrect"}
}
