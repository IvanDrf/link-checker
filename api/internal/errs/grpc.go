package errs

import (
	"encoding/json"
	"net/http"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

func HandlerGrpcError(w http.ResponseWriter, err error) {
	st, ok := status.FromError(err)
	if !ok {
		json.NewEncoder(w).Encode(ErrInternalServer())
		return
	}

	json.NewEncoder(w).Encode(Error{
		Code: grpcAndHttpCodes[st.Code()],
		Msg:  st.Message(),
	})
}

var grpcAndHttpCodes = map[codes.Code]int{
	codes.InvalidArgument:    http.StatusBadRequest,
	codes.NotFound:           http.StatusNotFound,
	codes.AlreadyExists:      http.StatusConflict,
	codes.PermissionDenied:   http.StatusForbidden,
	codes.Unauthenticated:    http.StatusUnauthorized,
	codes.ResourceExhausted:  http.StatusTooManyRequests,
	codes.FailedPrecondition: http.StatusPreconditionFailed,
	codes.OutOfRange:         http.StatusBadRequest,

	codes.Unimplemented:    http.StatusNotImplemented,
	codes.Unavailable:      http.StatusServiceUnavailable,
	codes.DeadlineExceeded: http.StatusGatewayTimeout,

	codes.Internal: http.StatusInternalServerError,
	codes.Unknown:  http.StatusInternalServerError,
	codes.DataLoss: http.StatusInternalServerError,
}
