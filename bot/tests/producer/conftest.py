from aio_pika import connect_robust
from pytest import fixture
from pytest_asyncio import fixture as async_fixture

from app.config.rabbitmq import RabbitmqConfig
from app.producer.producer import Producer
from app.schemas.message import LinkMessage, LinkStatus


@fixture
def rabbitmq_config(rabbitmq_proc) -> RabbitmqConfig:
    return RabbitmqConfig(
        username='guest',
        password='guest',
        host=rabbitmq_proc.host,
        port=rabbitmq_proc.port,
        cons_queue='test_produs', produs_queue='test_cons'
    )


@async_fixture
async def producer(rabbitmq_config: RabbitmqConfig):
    conn = await connect_robust(f'amqp://{rabbitmq_config.username}:{rabbitmq_config.password}@{rabbitmq_config.host}:{rabbitmq_config.port}/')
    chan = await conn.channel()
    queue = await chan.declare_queue(name=rabbitmq_config.produs_queue, durable=False, auto_delete=True)

    produs = Producer(conn, chan, queue)

    yield produs
    await produs.close()


@fixture(scope='package')
def links() -> LinkMessage:
    return LinkMessage(
        user_id=1234567,
        chat_id=456789,
        links=(
            LinkStatus(link='google.com', status=True),
            LinkStatus(link='vk.com', status=True),
            LinkStatus(link='habr.com', status=True),
            LinkStatus(link='badlink', status=False),
            LinkStatus(link='123.fm', status=False),
        )
    )
