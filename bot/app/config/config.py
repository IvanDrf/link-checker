from typing import Final, Optional
from yaml import safe_load
from typing import Optional
from argparse import ArgumentParser, Namespace


default_config_path: Final = 'config/config.yaml'


class Config:
    __slots__ = ('logger_level', 'bot_token', 'storage_path')

    def __init__(self, logger_level: str, bot_token: str, storage_path: str) -> None:
        self.logger_level: Final = logger_level
        self.bot_token: Final = bot_token
        self.storage_path: Final = storage_path

    @classmethod
    def new(cls, config_path: Optional[str]) -> 'Config':
        if config_path is None:
            config_path = default_config_path

        with open(config_path, 'r') as config_file:
            data: dict[str, str] = safe_load(config_file)

            return cls(data['logger_level'], data['bot_token'], data['storage_path'])

    @staticmethod
    def get_config_path_from_flag() -> Optional[str]:
        parser: ArgumentParser = ArgumentParser()
        parser.add_argument('--config')
        args: Namespace = parser.parse_args()

        return args.config
