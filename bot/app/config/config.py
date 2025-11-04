from dataclasses import dataclass
from typing import Final, Optional, Any
from yaml import safe_load
from typing import Optional
from argparse import ArgumentParser, Namespace

default_config_path: Final = 'config/config.yaml'


@dataclass
class AppConfig:
    logger_level: str
    bot_token: str
    storage_path: str


@dataclass
class RabbitmqConfig:
    username: str
    password: str
    host: str
    port: str
    cons_queue: str
    produs_queue: str


@dataclass
class Config:
    app: AppConfig
    rabbitmq: RabbitmqConfig

    @classmethod
    def load(cls, config_path: Optional[str]) -> 'Config':
        if config_path is None or config_path == '':
            config_path = default_config_path

        with open(config_path, 'r') as config_file:
            data: dict[str, Any] = safe_load(config_file)

            rabbit: dict[str, Any] = data['rabbitmq']

            return cls(
                app=AppConfig(
                    logger_level=data['logger_level'],
                    bot_token=data['bot_token'],
                    storage_path=data['storage_path']),

                rabbitmq=RabbitmqConfig(
                    username=rabbit['username'],
                    password=rabbit['password'],
                    host=rabbit['host'],
                    port=rabbit['port'],
                    cons_queue=rabbit['consumer_queue'],
                    produs_queue=rabbit['producer_queue'])
            )

    @staticmethod
    def get_config_path_from_flag() -> Optional[str]:
        parser: ArgumentParser = ArgumentParser()
        parser.add_argument('--config')
        args: Namespace = parser.parse_args()

        return args.config
