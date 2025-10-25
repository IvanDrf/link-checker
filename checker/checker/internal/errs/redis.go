package errs

func ErrCantSaveLinks() error {
	return Error{Msg: "cant save links to redis"}
}

func ErrLinkNotInRedis() error {
	return Error{Msg: "link is not in the redis"}
}

func ErrCantGetLink() error {
	return Error{Msg: "cant get link from redis"}
}
