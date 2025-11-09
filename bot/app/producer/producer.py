from aio_pika import connect_robust, Message, DeliveryMode
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel, AbstractMessage

from app.config.config import Config
from app.models.rabbitmq import LinkRequest


class Producer:
    def __init__(self, conn: AbstractRobustConnection, queue_name: str) -> None:
        self.conn: AbstractRobustConnection = conn
        self.queue_name: str = queue_name

        self.chan:  AbstractRobustChannel = self.conn.channel()

    @classmethod
    async def new(cls, cfg: Config) -> 'Producer':
        conn: AbstractRobustConnection = await connect_robust(f'amqp://{cfg.rabbitmq.username}:{cfg.rabbitmq.password}@{cfg.rabbitmq.host}/')

        return cls(conn, cfg.rabbitmq.produs_queue)

    async def produce(self, links: LinkRequest) -> None:
        await self.chan.declare_queue(self.queue_name, durable=True)

        message: AbstractMessage = Message(
            body=links.model_dump_json().encode(), delivery_mode=DeliveryMode.PERSISTENT)
        await self.chan.default_exchange.publish(message, routing_key=self.queue_name)
