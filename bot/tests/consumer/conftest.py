from pytest import fixture
from pytest_asyncio import fixture as async_fixture

from aio_pika import connect_robust

from app.config.rabbitmq import RabbitmqConfig
from app.consumer.consumer import Consumer
from app.schemas.message import LinkMessage, LinkStatus


@fixture
def rabbitmq_config(rabbitmq_proc) -> RabbitmqConfig:
    return RabbitmqConfig(
        username='guest',
        password='guest',
        host=rabbitmq_proc.host,
        port=rabbitmq_proc.port,
        cons_queue='produs',
        produs_queue='cons',
    )


@async_fixture
async def consumer(rabbitmq_config: RabbitmqConfig):
    conn = await connect_robust(f'amqp://{rabbitmq_config.username}:{rabbitmq_config.password}@{rabbitmq_config.host}:{rabbitmq_config.port}/')
    chan = await conn.channel()
    queue = await chan.declare_queue(name=rabbitmq_config.cons_queue, durable=False, auto_delete=True)

    cons = Consumer(conn, chan, queue)

    yield cons
    await cons.close()


@fixture(scope='package')
def USER_ID() -> int:
    return 1234567


@fixture(scope='package')
def CHAT_ID() -> int:
    return 1234567


@fixture(scope='package')
def links(USER_ID: int, CHAT_ID: int) -> LinkMessage:
    return LinkMessage(
        user_id=USER_ID,
        chat_id=CHAT_ID,
        links=(
            LinkStatus(link='google.com', status=True),
            LinkStatus(link='vk.com', status=True),
            LinkStatus(link='habr.com', status=True),
            LinkStatus(link='badlink', status=False),
            LinkStatus(link='123.fm', status=False),
        )
    )
