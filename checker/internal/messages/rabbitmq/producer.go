package rabbitmq

import (
	"context"
	"encoding/json"
	"fmt"
	"log/slog"

	"github.com/IvanDrf/checker/internal/config"
	"github.com/IvanDrf/checker/internal/errs"
	"github.com/IvanDrf/checker/internal/models"
	rabbit "github.com/rabbitmq/amqp091-go"
)

type producer struct {
	conn  *rabbit.Connection
	ch    *rabbit.Channel
	queue *rabbit.Queue

	logger *slog.Logger
}

func NewProducer(cfg *config.Config, logger *slog.Logger) Producer {
	conn, ch := connectToRabbitmq(cfg)
	queue := declareQueue(cfg.Rabbitmq.ProdusQueue, ch)

	return &producer{
		conn:  conn,
		ch:    ch,
		queue: queue,

		logger: logger,
	}
}

func (p *producer) SendMessage(ctx context.Context, links *models.RabbitLinks) {
	linksBytes, _ := json.Marshal(*links)

	err := p.ch.PublishWithContext(ctx, "", p.queue.Name, false, false, rabbit.Publishing{
		ContentType: "text/plain",
		Body:        linksBytes,
	})

	if err != nil {
		p.logger.Error(errs.ErrCantSendMessage(p.queue.Name).Error())

	} else {
		p.logger.Info(fmt.Sprintf("Message send for %v", links.UserId))
	}
}

func (p *producer) Close() {
	p.logger.Info("producer -> Close")

	p.ch.Close()
	p.conn.Close()
}
