from dataclasses import dataclass

from app.config.config import Config

from app.commands.start.start import Starter
from app.commands.start.abstraction import IStarter

from app.commands.save.save import Saver
from app.commands.save.abstraction import ISaver

from app.commands.delete.delete import Deleter
from app.commands.delete.abstraction import IDeleter

from app.commands.my.my import MyLinker
from app.commands.my.abstraction import ILinker

from app.commands.check.abstraction import IChecker
from app.commands.check.check import Checker

from app.commands.csv.abstraction import ICsver
from app.commands.csv.csv import Csver

from app.fabric.repo import RepoFabric
from app.fabric.redis import RedisRepoFabric
from app.fabric.producer import ProducerFabric
from app.fabric.consumer import ConsumerFabric


@dataclass
class Dependencies:
    starter: IStarter
    saver: ISaver
    deleter: IDeleter
    my_linker: ILinker
    checker: IChecker
    csver: ICsver


class DependenciesFabric:
    @staticmethod
    async def create_handler_dependencies(cfg: Config) -> Dependencies:
        repo, redis_repo, producer, consumer = await DependenciesFabric._create_dependencies(cfg)

        starter: IStarter = Starter(repo)
        saver: ISaver = Saver(repo)
        deleter: IDeleter = Deleter(repo)
        my_linker: ILinker = MyLinker(repo)
        checker: IChecker = Checker(repo, redis_repo, consumer, producer)
        csver: ICsver = Csver(redis_repo)

        return Dependencies(starter, saver, deleter, my_linker, checker, csver)

    @staticmethod
    async def _create_dependencies(cfg: Config):
        repo = await RepoFabric.new_repo(cfg)
        redis_repo = await RedisRepoFabric.new_redis_repo(cfg)

        producer = await ProducerFabric.new_producer(cfg)
        consumer = await ConsumerFabric.new_consumer(cfg)

        return repo, redis_repo, producer, consumer
