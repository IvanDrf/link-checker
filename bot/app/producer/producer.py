from aio_pika import connect_robust, Message, DeliveryMode
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractMessage, AbstractQueue

from app.config.config import Config
from app.schemas.message import LinkMessage


class Producer:
    def __init__(self, conn: AbstractRobustConnection, chan: AbstractChannel, queue: AbstractQueue) -> None:
        self.conn: AbstractRobustConnection = conn
        self.chan: AbstractChannel = chan
        self.queue: AbstractQueue = queue

    @classmethod
    async def new(cls, cfg: Config) -> 'Producer':
        conn: AbstractRobustConnection = await connect_robust(f'amqp://{cfg.rabbitmq.username}:{cfg.rabbitmq.password}@{cfg.rabbitmq.host}/')
        chan: AbstractChannel = await conn.channel()
        queue: AbstractQueue = await chan.declare_queue(name=cfg.rabbitmq.produs_queue, durable=False)

        return cls(conn, chan, queue)

    async def close(self) -> None:
        if self.conn:
            await self.conn.close()

    async def produce(self, links: LinkMessage) -> None:
        message: AbstractMessage = Message(
            body=links.model_dump_json().encode(),
            delivery_mode=DeliveryMode.PERSISTENT
        )

        await self.chan.default_exchange.publish(message, routing_key=self.queue.name)
