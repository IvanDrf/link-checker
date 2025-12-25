from aio_pika import DeliveryMode, Message
from pytest import mark

from app.consumer.consumer import Consumer
from app.schemas.message import LinkMessage


@mark.asyncio
async def test_consumer(consumer: Consumer, links: LinkMessage, USER_ID: int, CHAT_ID: int) -> None:
    # send message to  consumer queue
    message = Message(
        body=links.model_dump_json().encode(),
        delivery_mode=DeliveryMode.PERSISTENT
    )

    await consumer.chan.default_exchange.publish(message=message, routing_key=consumer.queue.name)

    links_from_queue = await consumer.consume(USER_ID, CHAT_ID)

    assert links_from_queue is not None
    assert links_from_queue == links

    final_state = await consumer.queue.declare(timeout=0.1)
    assert final_state.message_count == 0
