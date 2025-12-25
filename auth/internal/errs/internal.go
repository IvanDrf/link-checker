package errs

import "fmt"

func ErrCantConnectToTCP(err error) error {
	return Error{
		Msg: fmt.Sprintf("internal error: %s", err.Error()),
	}
}

func ErrCantStartAuthServer(err error) error {
	return Error{
		Msg: fmt.Sprintf("cant start auth server: %s", err.Error()),
	}
}
