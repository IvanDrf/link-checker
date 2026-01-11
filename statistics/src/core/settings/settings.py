from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Final

from yaml import safe_load

from src.core.settings.app import AppSettings
from src.core.settings.postgresql import DatabaseSettings
from src.core.settings.redis import RedisSettings


DEFAULT_SETTIGS_PATH: Final = 'config/config.yaml'


@dataclass(frozen=True)
class Settings:
    app: AppSettings
    database: DatabaseSettings
    cache: RedisSettings

    @classmethod
    def __load_from_yaml(cls, path_to_yaml: str = DEFAULT_SETTIGS_PATH) -> 'Settings':
        with open(path_to_yaml, 'r') as file:
            content = safe_load(file)

            return Settings(
                app=AppSettings(**content['app']),
                database=DatabaseSettings(**content['database']),
                cache=RedisSettings(**content['cache'])
            )

    @staticmethod
    def load_settings() -> 'Settings':
        parser = ArgumentParser()
        parser.add_argument('-c', '--config')

        args, _ = parser.parse_known_args()
        if args.config:
            return Settings.__load_from_yaml(args.config)

        return Settings.__load_from_yaml()


settings = Settings.load_settings()
