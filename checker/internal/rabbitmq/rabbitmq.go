package rabbitmq

import (
	"context"

	"github.com/IvanDrf/checker/internal/models"
)

type Rabbiter interface {
	ReadMessages()
	ServiceMessages()
	SendMessages()

	GracefulStop()
}

type Producer interface {
	SendMessage(ctx context.Context, links *models.RabbitLinks)
	Close()
}

type Consumer interface {
	ReadMessages(tasksChan chan *models.RabbitLinks, doneConsuming chan struct{})
	Close()
}
