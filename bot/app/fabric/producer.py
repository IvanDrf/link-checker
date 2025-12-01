from app.commands.abstraction.producer import IProducer
from app.producer.producer import Producer
from app.config.config import Config


class ProducerFabric:
    @staticmethod
    async def new_producer(cfg: Config) -> IProducer:
        return await Producer.new(cfg)
