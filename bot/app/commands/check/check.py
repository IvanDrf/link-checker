from aiogram.types import Message
from aiogram.fsm.context import FSMContext

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

SENDING_TIME: Final = 3
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

    async def check_links(self, message: Message, state: FSMContext):
        await state.clear()

        if message.from_user is None:
            await message.answer('Cant get your id, please try again')
            return

        links: Optional[list[Link]] = await self.repo.find_links(message.from_user.id)
        if links is None:
            await message.answer('You dont have any saved links')
            return

        await self.send_message_from_producer(links, message.from_user.id, message.chat.id)
        res = await self.get_message_from_consumer(message.from_user.id, message.chat.id)
        logging.error(f'check -> {res}')
        return res

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

    async def _get_message_with_time(self, user_id: int, chat_id: int) -> Optional[LinkResponse]:
        async with timeout(RECEIVING_TIME):
            return await self.consumer.consume(user_id, chat_id)


def create_links_request(links: list[Link], user_id: int, chat_id: int) -> LinkRequest:
    return LinkRequest(
        user_id=user_id,
        chat_id=chat_id,
        links=[LinkStatus(link=link.link, status=False) for link in links]
    )
