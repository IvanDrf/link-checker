package errs

import "fmt"

func ErrCantSendMessage(queue string) error {
	return Error{
		Msg: fmt.Sprintf("cant send message on queue: %s", queue),
	}
}

func ErrCantReadMessages(queue string) error {
	return Error{
		Msg: fmt.Sprintf("cant read messages from %s", queue),
	}
}

func ErrCantUnmarshalMessage() error {
	return Error{
		Msg: "cant unmarshal message from rabbitmq",
	}
}
