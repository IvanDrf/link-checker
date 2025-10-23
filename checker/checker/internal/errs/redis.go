package errs

import "fmt"

func ErrCantAddLink(link *string) error {
	return Error{Msg: fmt.Sprintf("cant add link: %s to redis", *link)}
}

func ErrLinkNotInRedis() error {
	return Error{Msg: "link is not in the redis"}
}

func ErrCantGetLink() error {
	return Error{Msg: "cant get link from redis"}
}
