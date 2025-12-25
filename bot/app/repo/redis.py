import logging
from json import dumps
from typing import Optional

from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.exc.internal import InternalError
from app.schemas.message import LinkMessage, LinkStatus, LinkTuple


class RedisRepo:
    def __init__(self, redis: Redis) -> None:
        self.redis: Redis = redis

    async def save_links(self, user_id: int, links: LinkMessage) -> None:
        links_json = dumps(tuple(link.model_dump() for link in links.links))

        try:
            await self.redis.set(name=str(user_id), value=links_json)
        except RedisError as e:
            logging.error(f'redis error -> {e.__str__()}')
            raise InternalError('cant save links in redis')

    async def get_links(self, user_id: int) -> tuple[LinkStatus, ...]:
        try:
            links_json: Optional[str] = await self.redis.get(str(user_id))
            if links_json is None:
                return tuple()

            return parse_links_json(links_json)

        except RedisError as e:
            logging.error(f'redis error -> {e.__str__()}')
            raise InternalError(f'cant get links for user:{user_id}')

    async def close(self) -> None:
        await self.redis.close()


def parse_links_json(links_json: str) -> tuple[LinkStatus, ...]:
    return LinkTuple.validate_json(links_json)
