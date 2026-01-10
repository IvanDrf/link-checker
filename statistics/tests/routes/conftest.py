from pytest import fixture

from src.schemas.link import Link


class LinkServiceTest:
    def __init__(self) -> None:
        self.links: dict[str, Link] = {}

    async def add_links(self, links: tuple[Link, ...]) -> None:
        for link in links:
            if link.link not in self.links:
                link.views = 1
                self.links[link.link] = link
            else:
                self.links[link.link].views += 1
                self.links[link.link].status = link.status

    async def get_most_popular_links(self, limit: int) -> tuple[Link, ...]:
        return tuple(sorted(self.links.values(), key=lambda arg: arg.views, reverse=True)[:limit])

    async def stop(self) -> None:
        pass


@fixture(scope='package')
def contents() -> list[dict]:
    return [
        {
            'link': 'google.com',
            'status': True
        },
        {
            'link': 'habr.com',
            'status': True
        },
        {
            'link': 'steam.com',
            'status': True
        },
        {
            'link': 'test.com',
            'status': False
        }
    ]
