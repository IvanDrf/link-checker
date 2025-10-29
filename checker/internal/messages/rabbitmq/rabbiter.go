package rabbitmq

import (
	"context"
	"log/slog"
	"time"

	"github.com/IvanDrf/checker/internal/config"
	"github.com/IvanDrf/checker/internal/infrastructure/semaphore"
	"github.com/IvanDrf/checker/internal/messages"
	"github.com/IvanDrf/checker/internal/models"
	"github.com/IvanDrf/checker/internal/service"
	linkService "github.com/IvanDrf/checker/internal/service/links"
	"github.com/redis/go-redis/v9"
)

type Producer interface {
	SendMessage(ctx context.Context, links *models.RabbitLinks)
	Close()
}

type Consumer interface {
	ReadMessages(tasksChan chan *models.RabbitLinks, doneConsuming chan struct{})
	Close()
}

type rabbiter struct {
	producer      Producer
	doneProducing chan struct{}

	consumer      Consumer
	doneConsuming chan struct{}

	linkChecker service.LinkChecker
	sem         semaphore.Semaphore

	tasksChan   chan *models.RabbitLinks
	resultsChan chan *models.RabbitLinks

	logger *slog.Logger
}

const (
	tasksChanLength   = 15
	resultsChanLength = 15

	semaphoreSize = 20
)

func NewRabbiter(cfg *config.Config, rdb *redis.Client, logger *slog.Logger) messages.Messenger {
	return &rabbiter{
		producer:      NewProducer(cfg, logger),
		doneProducing: make(chan struct{}, 1),

		consumer:      NewConsumer(cfg, rdb, logger),
		doneConsuming: make(chan struct{}, 1),

		linkChecker: linkService.NewLinkChecker(rdb, logger),
		sem:         semaphore.NewSemaphore(semaphoreSize),

		tasksChan:   make(chan *models.RabbitLinks, tasksChanLength),
		resultsChan: make(chan *models.RabbitLinks, resultsChanLength),

		logger: logger,
	}
}

func (r *rabbiter) ReadMessages() {
	r.consumer.ReadMessages(r.tasksChan, r.doneConsuming)
}

const serviceTime = 5 * time.Second

func (r *rabbiter) ServiceMessages() {
	for {
		select {
		case links, ok := <-r.tasksChan:
			if !ok {
				return
			}
			r.logger.Info("rabbiter -> get message from tasks chan")

			ctx, cancel := context.WithTimeout(context.Background(), serviceTime)
			defer cancel()

			go func(links *models.RabbitLinks) {
				r.logger.Info("rabbiter -> start servicing message")

				r.sem.Acquire()
				defer r.sem.Release()

				r.serviceMessage(ctx, links)

				r.logger.Info("rabbiter -> send message to results chan")
				r.resultsChan <- links
			}(links)
		case <-r.doneConsuming:
			r.logger.Info("rabbiter -> done consuming")
			return
		}
	}
}

func (r *rabbiter) serviceMessage(ctx context.Context, links *models.RabbitLinks) {
	if len(links.Links) > service.MaxLinksCount {
		links.Links = nil
		return
	}

	stringLinks := convertRabbitLinksToStrings(links)

	links.Links = r.linkChecker.CheckLinks(ctx, stringLinks)
}

func convertRabbitLinksToStrings(links *models.RabbitLinks) []string {
	stringLinks := make([]string, 0, len(links.Links))

	for i := range links.Links {
		stringLinks = append(stringLinks, links.Links[i].Link)
	}

	return stringLinks
}

const sendingTime = 2 * time.Second

func (r *rabbiter) SendMessages() {
	for {
		select {
		case links, ok := <-r.resultsChan:
			if !ok {
				return
			}
			r.logger.Info("rabbiter -> get message from results chan")

			ctx, cancel := context.WithTimeout(context.Background(), sendingTime)
			defer cancel()

			r.logger.Info("rabbiter -> send message to producer")
			r.producer.SendMessage(ctx, links)

		case <-r.doneProducing:
			r.logger.Info("rabbiter -> done producing")
			return
		}
	}
}

func (r *rabbiter) GracefulStop() {
	r.logger.Info("rabbiter -> GracefulStop")
	r.consumer.Close()
	r.producer.Close()

	r.doneConsuming <- struct{}{}
	r.doneProducing <- struct{}{}
}
