package errs

func ErrTooManyUrls() error {
	return Error{Msg: "too many links in request"}
}
