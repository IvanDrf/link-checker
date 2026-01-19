from typing import Any, AsyncGenerator

from src.schemas.link import Link
from src.service.links import LinkService


async def get_links_with_limit(link_service: LinkService, limits: tuple[int, ...]) -> AsyncGenerator[tuple[tuple[Link, ...], int], Any]:
    for limit in limits:
        links: tuple[Link, ...] = await link_service.get_most_popular_links(limit)

        yield links, limit
