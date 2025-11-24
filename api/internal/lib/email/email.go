package email

import (
	"bytes"
	"html/template"
	"log"
	"net/smtp"

	"github.com/IvanDrf/api-gateway/internal/config"
	"github.com/IvanDrf/api-gateway/internal/errs"
)

type EmailSender interface {
	SendVerificationEmail(email string, link string) error
}

type emailSender struct {
	addr string
	port string

	hostAddr string
	username string
	password string
}

func NewEmailSender(cfg *config.Config) EmailSender {
	return &emailSender{
		addr: cfg.Api.Addr,
		port: cfg.Api.Port,

		hostAddr: cfg.Email.HostAddr,
		username: cfg.Email.Username,
		password: cfg.Email.Password,
	}
}

func (e *emailSender) SendVerificationEmail(email string, link string) error {
	message := createVerificationMessage(link)
	if message == "" {
		return errs.ErrCantCreateEmailMessage()
	}

	auth := smtp.PlainAuth("", e.username, e.password, "smtp.gmail.com")

	err := smtp.SendMail(e.hostAddr, auth, e.username, []string{email}, []byte(message))
	if err != nil {
		log.Println(err)
		return errs.ErrCantSendEmail(email)
	}

	return nil
}

const (
	htmlEmailBodyPath = "static/verify.html"
	headers           = "MIME-version: 1.0;\nContent-Type: text/html; charset=\"UTF-8\";"
)

func createVerificationMessage(link string) string {
	tmpl, err := template.ParseFiles(htmlEmailBodyPath)
	if err != nil {
		return ""
	}

	buff := bytes.Buffer{}
	err = tmpl.Execute(&buff, struct{ Link string }{Link: link})
	if err != nil {
		return ""
	}

	return headers + "\n\n" + buff.String()
}
