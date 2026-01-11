from typing import Optional

from pytest import mark
from redis.asyncio import Redis

from src.repo.cache import LINKS_KEY, CacheRepo, format_links_to_json


def test_format_links_to_json(links, links_json) -> None:
    links_json_from_format = format_links_to_json(links)
    assert links_json_from_format == links_json


@mark.asyncio
async def test_save_links(cache_repo: CacheRepo, redis: Redis, links, links_json) -> None:
    await cache_repo.save_links(links)

    links_json_from_cache: Optional[bytes] = await redis.get(LINKS_KEY)

    assert links_json_from_cache is not None
    assert links_json_from_cache.decode() == links_json


@mark.asyncio
async def test_get_links(cache_repo: CacheRepo, links) -> None:
    await cache_repo.save_links(links)

    links_from_cache = await cache_repo.get_links()
    assert links_from_cache == links
