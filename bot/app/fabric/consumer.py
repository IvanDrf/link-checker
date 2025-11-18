from app.consumer.abstraction import IConsumer
from app.consumer.consumer import Consumer
from app.config.config import Config


class ConsumerFabric:
    @staticmethod
    async def new_consumer(cfg: Config) -> IConsumer:
        return await Consumer.new(cfg)
