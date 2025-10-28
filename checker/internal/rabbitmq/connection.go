package rabbitmq

import (
	"fmt"
	"log"

	"github.com/IvanDrf/checker/internal/config"
	rabbit "github.com/rabbitmq/amqp091-go"
)

func ConnectToRabbitmq(cfg *config.Config) (*rabbit.Connection, *rabbit.Channel) {
	conn, err := rabbit.Dial(fmt.Sprintf("amqp://%s:%s@%s:%s/", cfg.Rabbitmq.Username, cfg.Rabbitmq.Password, cfg.Rabbitmq.Host, cfg.Rabbitmq.Port))
	if err != nil {
		log.Fatal(err)
	}

	ch, err := conn.Channel()
	if err != nil {
		log.Fatal(err)
	}

	return conn, ch
}

func DeclareQueue(name string, ch *rabbit.Channel) *rabbit.Queue {
	queue, err := ch.QueueDeclare(name, false, false, false, false, nil)
	if err != nil {
		log.Fatal(err)
	}

	return &queue
}
