package errs

import "fmt"

func ErrCantCreateEmailMessage() error {
	return Error{
		Msg: "cant create message for email",
	}
}

func ErrCantSendEmail(email string) error {
	return Error{
		Msg: fmt.Sprintf("cant send email to %s", email),
	}
}
