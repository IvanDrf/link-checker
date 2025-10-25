package errs

import "net/http"

func ErrUnsupportedMediaType() error {
	return Error{
		Code: http.StatusUnsupportedMediaType,
		Msg:  "unsupported media type, want - json",
	}
}

func ErrInvalidJSON() error {
	return Error{
		Code: http.StatusBadRequest,
		Msg:  "invalid json",
	}
}

func ErrInternalServer() error {
	return Error{
		Code: http.StatusInternalServerError,
		Msg:  "internal server error",
	}
}
