from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractQueue, AbstractIncomingMessage
from pydantic import ValidationError

from typing import Optional
import logging

from app.config.config import Config
from app.models.message import LinkMessage


class Consumer:
    def __init__(self, conn: AbstractRobustConnection, chan: AbstractChannel, queue: AbstractQueue) -> None:
        self.conn: AbstractRobustConnection = conn
        self.chan: AbstractChannel = chan
        self.queue: AbstractQueue = queue

    @classmethod
    async def new(cls, cfg: Config) -> 'Consumer':
        conn: AbstractRobustConnection = await connect_robust(f'amqp://{cfg.rabbitmq.username}:{cfg.rabbitmq.password}@{cfg.rabbitmq.host}/')
        chan: AbstractChannel = await conn.channel()
        queue: AbstractQueue = await chan.declare_queue(name=cfg.rabbitmq.cons_queue, durable=False)

        return cls(conn, chan, queue)

    async def close(self) -> None:
        if self.conn:
            await self.conn.close()

    async def consume(self, user_id: int, chat_id: int) -> Optional[LinkMessage]:
        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                links: Optional[LinkMessage] = parse_incoming_message(message)
                if links is None:
                    await message.nack(requeue=False)
                    continue

                if check_message_for_user(links, user_id, chat_id):
                    await message.ack()
                    return links
                else:
                    await message.nack(requeue=True)

        return None


def parse_incoming_message(message: AbstractIncomingMessage) -> Optional[LinkMessage]:
    try:
        links: LinkMessage = LinkMessage.model_validate_json(
            message.body.decode())

        return links

    except ValidationError:
        logging.error('consumer -> get invalid message from rabbitmq')
        return None


def check_message_for_user(links: LinkMessage, user_id: int, chat_id: int) -> bool:
    return links.user_id == user_id and links.chat_id == chat_id
