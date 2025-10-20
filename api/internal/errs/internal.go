package errs

import "fmt"

func ErrCantFindConfigFile(cfgPath string) error {
	return Error{
		Code: 0,
		Msg:  fmt.Sprintf("cant find config file %s", cfgPath),
	}
}

func ErrCantParseConfigFile(err error) error {
	return Error{
		Code: 0,
		Msg:  fmt.Sprintf("cant parse config file %v", err.Error()),
	}
}

func ErrCantStartServer(err error) error {
	return Error{
		Code: 0,
		Msg:  fmt.Sprintf("cant start server on cfg port, error: %s", err.Error()),
	}
}
