package errs

import "fmt"

func ErrVerifTokenDoesntExist(link string) error {
	return Error{
		Msg: fmt.Sprintf("this verification token doesnt exist: %s", link),
	}
}

func ErrCantGetVerifTokenFromRedis(link string) error {
	return Error{
		Msg: fmt.Sprintf("cant get verification token from redis: %s", link),
	}
}

func ErrCantSaveVerifToken() error {
	return Error{
		Msg: "cant save verification token",
	}
}
