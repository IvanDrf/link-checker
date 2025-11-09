from aio_pika import connect_robust
from aio_pika.abc import AbstractRobustConnection, AbstractChannel, AbstractQueue
from typing import Optional

from app.config.config import Config
from app.models.rabbitmq import LinkResponse


class Consumer:
    def __init__(self, conn: AbstractRobustConnection, queue_name: str) -> None:
        self.conn: AbstractRobustConnection = conn
        self.queue_name: str = queue_name

        self.chan: AbstractChannel = self.conn.channel()

    @classmethod
    async def new(cls, cfg: Config) -> 'Consumer':
        conn: AbstractRobustConnection = await connect_robust(f'amqp://{cfg.rabbitmq.username}:{cfg.rabbitmq.password}@{cfg.rabbitmq.host}/')

        return cls(conn, cfg.rabbitmq.cons_queue)

    async def consume(self, user_id: int, chat_id: int) -> Optional[LinkResponse]:
        queue: AbstractQueue = await self.chan.declare_queue(name=self.queue_name)

        return await self._read_messages(queue, user_id, chat_id)

    async def _read_messages(self, queue: AbstractQueue, user_id: int, chat_id: int) -> Optional[LinkResponse]:
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():

                    links: LinkResponse = LinkResponse.model_validate_json(
                        message.body.decode())

                if links.user_id == user_id and links.chat_id == chat_id:
                    return links

                await message.ack()

        return None
