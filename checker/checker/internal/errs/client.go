package errs

func ErrTooManyUrls() error {
	return Error{Msg: "too many urls in request"}
}
