import logging
from asyncio import create_task, timeout
from typing import Final, Optional

from app.commands.abstraction.consumer import IConsumer
from app.commands.abstraction.producer import IProducer
from app.commands.abstraction.repo import IRedisRepo, IRepo
from app.exc.external import ExternalError
from app.exc.internal import InternalError
from app.exc.user import UserError
from app.models.link import Link
from app.schemas.message import LinkMessage, LinkStatus


WAITING_TIME: Final = 1
SENDING_TIME: Final = 2
RECEIVING_TIME: Final = 5


class Checker:
    def __init__(self, repo: IRepo, redis_repo: IRedisRepo, consumer: IConsumer, producer: IProducer) -> None:
        self.repo: IRepo = repo
        self.redis_repo: IRedisRepo = redis_repo

        self.consumer: IConsumer = consumer
        self.producer: IProducer = producer

    async def close(self) -> None:
        await self.redis_repo.close()

        await self.consumer.close()
        await self.producer.close()

    async def check_links(self, user_id: int, chat_id: int) -> str:
        links: Optional[tuple[Link, ...]] = await self.repo.find_links(user_id)
        if links is None:
            raise UserError('You dont have any saved links')

        links_from_queue: Optional[LinkMessage] = await self._check_for_links_in_queue(user_id, chat_id)
        if not links_from_queue is None:
            create_task(self.redis_repo.save_links(user_id, links_from_queue))
            return create_links_response(links_from_queue)

        await self._send_message_from_producer(links, user_id, chat_id)

        res: Optional[LinkMessage] = await self._get_message_from_consumer(user_id, chat_id)
        if res is None:
            raise ExternalError('Cant get message from Link-Checker service')

        create_task(self.redis_repo.save_links(user_id, res))
        return create_links_response(res)

    async def _check_for_links_in_queue(self, user_id: int, chat_id: int) -> Optional[LinkMessage]:
        try:
            return await self._get_message_with_time(user_id, chat_id, WAITING_TIME)
        except (InternalError, TimeoutError):
            logging.info('there are no pending messages')

        return None

    async def _send_message_from_producer(self, links: tuple[Link, ...], user_id: int, chat_id: int) -> None:
        try:
            links_req: LinkMessage = create_links_request(
                links, user_id, chat_id)

            await self._send_message_with_time(links_req)

        except TimeoutError:
            logging.error('timeout for sending message from producer')
            raise InternalError('cant send message to Link-Checker service')

    async def _send_message_with_time(self, links_req: LinkMessage) -> None:
        async with timeout(SENDING_TIME):
            await self.producer.produce(links_req)

    async def _get_message_from_consumer(self, user_id: int, chat_id: int) -> Optional[LinkMessage]:
        try:
            return await self._get_message_with_time(user_id, chat_id)

        except TimeoutError:
            logging.error(
                'timeout for receiving message form Link-Checker service')
            raise InternalError(
                'cant receive message from Link-Checker service')

    async def _get_message_with_time(self, user_id: int, chat_id: int, receiving_time: float = RECEIVING_TIME) -> Optional[LinkMessage]:
        async with timeout(receiving_time):
            return await self.consumer.consume(user_id, chat_id)


def create_links_request(links: tuple[Link, ...], user_id: int, chat_id: int) -> LinkMessage:
    return LinkMessage(
        user_id=user_id,
        chat_id=chat_id,
        links=tuple(LinkStatus(link=link.link, status=False) for link in links)
    )


def create_links_response(links: LinkMessage) -> str:
    return '\n'.join(f'{link.link} - {'✅' if link.status else '❌'}' for link in links.links)
