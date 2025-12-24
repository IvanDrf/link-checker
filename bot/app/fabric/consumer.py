from app.commands.abstraction.consumer import IConsumer
from app.config.config import Config
from app.consumer.consumer import Consumer


class ConsumerFabric:
    @staticmethod
    async def new_consumer(cfg: Config) -> IConsumer:
        return await Consumer.new(cfg)
