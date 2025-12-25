from pytest import mark

from asyncio import sleep

from app.producer.producer import Producer
from app.schemas.message import LinkMessage


@mark.asyncio
async def test_producer(producer: Producer, links: LinkMessage) -> None:
    await producer.produce(links)

    message = await producer.queue.get(timeout=0.5)
    await message.ack()

    link_from_queue = LinkMessage.model_validate_json(message.body.decode())
    assert link_from_queue == links
