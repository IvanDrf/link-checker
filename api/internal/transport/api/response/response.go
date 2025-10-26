package response

import (
	"encoding/json"
	"github.com/IvanDrf/api-gateway/internal/errs"
	"net/http"
)

func RespondUnsupportedMedia(w http.ResponseWriter) {
	w.WriteHeader(http.StatusUnsupportedMediaType)

	json.NewEncoder(w).Encode(errs.ErrUnsupportedMediaType())
}

func RespondBadRequest(w http.ResponseWriter) {
	w.WriteHeader(http.StatusBadRequest)

	json.NewEncoder(w).Encode(errs.ErrInvalidJSON())
}
