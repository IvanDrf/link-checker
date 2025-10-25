package errs

func ErrTooManyLinksInRequest() error {
	return Error{Msg: "too many links in request"}
}
