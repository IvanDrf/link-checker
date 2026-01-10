from pytest import fixture

from src.schemas.link import Link


@fixture(scope='session')
def links() -> tuple[Link, ...]:
    return (
        Link(link='google.com', status=True, views=10),
        Link(link='vk.com', status=True, views=1),
        Link(link='ya.ru', status=True, views=2),
        Link(link='habr.com', status=True, views=3),
        Link(link='test.com', status=True, views=6)
    )
