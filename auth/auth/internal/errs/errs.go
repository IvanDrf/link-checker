package errs

import "fmt"

type Error struct {
	Code int
	Msg  string
}

func (e Error) Error() string {
	return fmt.Sprintf("code: %v, msg: %s", e.Code, e.Msg)
}
