package rabbitmq

import (
	"encoding/json"
	"log"
	"log/slog"

	"github.com/IvanDrf/checker/internal/config"
	"github.com/IvanDrf/checker/internal/errs"
	"github.com/IvanDrf/checker/internal/models"
	"github.com/IvanDrf/checker/internal/service"
	linkService "github.com/IvanDrf/checker/internal/service/links"
	rabbit "github.com/rabbitmq/amqp091-go"
	"github.com/redis/go-redis/v9"
)

type consumer struct {
	conn  *rabbit.Connection
	ch    *rabbit.Channel
	queue *rabbit.Queue

	checker service.LinkChecker

	logger *slog.Logger
}

func NewConsumer(cfg *config.Config, db *redis.Client, logger *slog.Logger) Consumer {
	conn, ch := connectToRabbitmq(cfg)
	queue := declareQueue(cfg.Rabbitmq.ConsQueue, ch)

	return &consumer{
		conn:  conn,
		ch:    ch,
		queue: queue,

		checker: linkService.NewLinkChecker(db, logger),
		logger:  logger,
	}
}

func (c *consumer) ReadMessages(tasksChan chan *models.RabbitLinks, doneConsuming chan struct{}) {
	messages := c.startConsuming()

	for message := range messages {
		select {
		case <-doneConsuming:
			return
		default:
			c.logger.Info("consumer -> get message")
			links := c.parseMessage(&message)
			if links == nil {
				c.logger.Warn("consumer -> get invalid message")
				message.Reject(false)
				continue
			}

			c.logger.Info("consumer -> send message to tasks chan")

			tasksChan <- links
			message.Ack(false)
		}
	}
}

func (c *consumer) startConsuming() <-chan rabbit.Delivery {
	messages, err := c.ch.Consume(c.queue.Name, "", false, false, false, false, nil)
	if err != nil {
		log.Fatal(errs.ErrCantReadMessages(c.queue.Name))
	}

	return messages
}

func (c *consumer) parseMessage(message *rabbit.Delivery) *models.RabbitLinks {
	links := models.RabbitLinks{}

	err := json.Unmarshal(message.Body, &links)
	if err != nil {
		c.logger.Error(errs.ErrCantUnmarshalMessage().Error())
		return nil
	}

	return &links
}

func (c *consumer) Close() {
	c.logger.Info("consumer -> Close")

	c.ch.Close()
	c.conn.Close()
}
