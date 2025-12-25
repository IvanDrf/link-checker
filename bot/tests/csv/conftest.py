from pytest import fixture

from app.schemas.message import LinkStatus


@fixture
def USER_ID() -> int:
    return 12345678


@fixture
def links() -> tuple[LinkStatus, ...]:
    return (LinkStatus(link='google.com', status=True),
            LinkStatus(link='ya.ru', status=True),
            LinkStatus(link='habr.com', status=True),
            LinkStatus(link='bad-link.com', status=False)
            )
