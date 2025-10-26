package errs

import "fmt"

type Error struct {
	Msg string
}

func (e Error) Error() string {
	return fmt.Sprintf("msg: %s", e.Msg)
}
