from pytest import fixture

from src.schemas.link import Link


@fixture(scope='session')
def repeated() -> int:
    '''repeated requests, inserts in database'''
    return 3


@fixture(scope='session')
def links() -> tuple[Link, ...]:
    return tuple(sorted([
        Link(link='google.com', status=True, views=10),
        Link(link='test.com', status=False, views=6),
        Link(link='habr.com', status=True, views=3),
        Link(link='ya.ru', status=True, views=2),
        Link(link='vk.com', status=True, views=1)],

        key=lambda arg: arg.views)
    )


@fixture(scope='session')
def limits(links: tuple[Link, ...], repeated: int) -> tuple[int, ...]:
    return tuple((len(links) - i) for i in range(repeated))
