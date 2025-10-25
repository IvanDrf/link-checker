package errs

import (
	"fmt"
	"net/http"
	"strconv"
	"strings"
)

type Error struct {
	Code int
	Msg  string
}

func (e Error) Error() string {
	return fmt.Sprintf("Code: %v, Msg: %s", e.Code, e.Msg)
}

// err MUST come from Error
func GetCode(err error) int {
	s := strings.Split(err.Error(), " ")
	if len(s) < 2 {
		return http.StatusBadRequest
	}

	strCode := s[1][:len(s[1])-1]
	code, _ := strconv.Atoi(strCode)

	return code
}
