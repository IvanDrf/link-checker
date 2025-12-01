from dataclasses import dataclass
from typing import Final, Optional, Any
from yaml import safe_load
from typing import Optional
from argparse import ArgumentParser, Namespace

from app.config.app import AppConfig
from app.config.rabbitmq import RabbitmqConfig
from app.config.redis import RedisConfig

DEFAULT_CONFIG_PATH: Final = 'config/config.yaml'


@dataclass(frozen=True)
class Config:
    app: AppConfig
    rabbitmq: RabbitmqConfig
    redis: RedisConfig

    @classmethod
    def load(cls, config_path: Optional[str]) -> 'Config':
        if config_path is None or config_path == '':
            config_path = DEFAULT_CONFIG_PATH

        return Config.read_config(config_path)

    @classmethod
    def read_config(cls, config_path: str) -> 'Config':
        with open(config_path, 'r') as config_file:
            data: dict[str, Any] = safe_load(config_file)

            rabbit: dict[str, Any] = data['rabbitmq']
            redis: dict[str, Any] = data['redis']

            return cls(
                app=AppConfig.read_config(data),
                rabbitmq=RabbitmqConfig.read_config(rabbit),
                redis=RedisConfig.read_config(redis)
            )

    @staticmethod
    def get_config_path_from_flag() -> Optional[str]:
        parser: ArgumentParser = ArgumentParser()
        parser.add_argument('--config')
        args: Namespace = parser.parse_args()

        return args.config
