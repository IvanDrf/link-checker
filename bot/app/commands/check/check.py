from asyncio import timeout
from typing import Optional, Final
import logging

from app.config.config import Config
from app.repo.repo import Repo
from app.models.link import Link
from app.models.rabbitmq import LinkStatus, LinkRequest, LinkResponse
from app.consumer.consumer import Consumer
from app.producer.producer import Producer
from app.exc.internal import InternalError

WAITING_TIME: Final = 1
SENDING_TIME: Final = 2
RECEIVING_TIME: Final = 5


class Checker:
    def __init__(self, repo: Repo, consumer: Consumer, producer: Producer) -> None:
        self.repo: Repo = repo
        self.consumer: Consumer = consumer
        self.producer: Producer = producer

    @classmethod
    async def new(cls, cfg: Config, repo: Repo) -> 'Checker':
        consumer: Consumer = await Consumer.new(cfg)
        producer: Producer = await Producer.new(cfg)

        return cls(repo, consumer, producer)

    async def check_links(self, user_id: int, chat_id: int) -> str:
        links: Optional[list[Link]] = await self.repo.find_links(user_id)
        if links is None:
            return 'You dont have any saved links'

        links_from_queue: Optional[LinkResponse] = await self.check_for_links_in_queue(user_id, chat_id)
        if not links_from_queue is None:
            return create_links_response(links_from_queue)

        await self.send_message_from_producer(links, user_id, chat_id)

        res: Optional[LinkResponse] = await self.get_message_from_consumer(user_id, chat_id)
        if res is None:
            return 'Cant get message from Link-Checker service'

        return create_links_response(res)

    async def check_for_links_in_queue(self, user_id: int, chat_id: int) -> Optional[LinkResponse]:
        try:
            return await self._get_message_with_time(user_id, chat_id, WAITING_TIME)
        except InternalError:
            logging.info('there are no pending messages')

        except TimeoutError:
            logging.info('there are no pending messages')

        return None

    async def send_message_from_producer(self, links: list[Link], user_id: int, chat_id: int) -> None:
        try:
            links_req: LinkRequest = create_links_request(
                links, user_id, chat_id)

            await self._send_message_with_time(links_req)

        except TimeoutError:
            logging.error('timeout for sending message from producer')
            raise InternalError('cant send message to Link-Checker service')

    async def _send_message_with_time(self, links_req: LinkRequest) -> None:
        async with timeout(SENDING_TIME):
            await self.producer.produce(links_req)

    async def get_message_from_consumer(self, user_id: int, chat_id: int) -> Optional[LinkResponse]:
        try:
            return await self._get_message_with_time(user_id, chat_id)

        except TimeoutError:
            logging.error(
                'timeout for receiving message form Link-Checker service')
            raise InternalError(
                'cant receive message from Link-Checker service')

    async def _get_message_with_time(self, user_id: int, chat_id: int, receiving_time: float = RECEIVING_TIME) -> Optional[LinkResponse]:
        async with timeout(receiving_time):
            return await self.consumer.consume(user_id, chat_id)


def create_links_request(links: list[Link], user_id: int, chat_id: int) -> LinkRequest:
    return LinkRequest(
        user_id=user_id,
        chat_id=chat_id,
        links=tuple(LinkStatus(link=link.link, status=False) for link in links)
    )


def create_links_response(links: LinkResponse) -> str:
    return '\n'.join(f'{link.link} - {'✅' if link.status else '❌'}' for link in links.links)
