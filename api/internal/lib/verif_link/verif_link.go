package veriflink

import (
	"fmt"

	"github.com/IvanDrf/api-gateway/internal/config"
)

type VerifLinkCreator interface {
	CreateVerificationLink(verifToken string) string
}

type verifLinkCreator struct {
	addr string
	port string
	path string
}

func NewVerifLinkCreator(cfg *config.Config, path string) VerifLinkCreator {
	return &verifLinkCreator{
		addr: cfg.Api.Addr,
		port: cfg.Api.Port,
		path: path,
	}
}

func (v *verifLinkCreator) CreateVerificationLink(verifToken string) string {
	return fmt.Sprintf("http://%s:%s/%s/?token=%s", v.addr, v.port, v.path, verifToken)
}
