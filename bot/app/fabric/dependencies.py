from dataclasses import dataclass

from app.config.config import Config

from app.commands.start.start import Starter
from app.commands.save.save import Saver
from app.commands.delete.delete import Deleter
from app.commands.my.my import MyLinker
from app.commands.check.check import Checker
from app.commands.csv.csv import Csver

from app.fabric.repo import RepoFabric
from app.fabric.redis import RedisRepoFabric
from app.fabric.producer import ProducerFabric
from app.fabric.consumer import ConsumerFabric


@dataclass
class Dependencies:
    starter: Starter
    saver: Saver
    deleter: Deleter
    my_linker: MyLinker
    checker: Checker
    csver: Csver


class DependenciesFabric:
    @staticmethod
    async def create_handler_dependencies(cfg: Config) -> Dependencies:
        repo, redis_repo, producer, consumer = await DependenciesFabric._create_dependencies(cfg)

        starter: Starter = Starter(repo)
        saver: Saver = Saver(repo)
        deleter: Deleter = Deleter(repo)
        my_linker: MyLinker = MyLinker(repo)
        checker: Checker = Checker(repo, redis_repo, consumer, producer)
        csver: Csver = Csver(redis_repo)

        return Dependencies(starter, saver, deleter, my_linker, checker, csver)

    @staticmethod
    async def _create_dependencies(cfg: Config):
        repo = await RepoFabric.new_repo(cfg)
        redis_repo = await RedisRepoFabric.new_redis_repo(cfg)

        producer = await ProducerFabric.new_producer(cfg)
        consumer = await ConsumerFabric.new_consumer(cfg)

        return repo, redis_repo, producer, consumer
