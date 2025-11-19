package errs

func ErrCantCreateVerifToken() error {
	return Error{
		Msg: "cant create verification token",
	}
}
