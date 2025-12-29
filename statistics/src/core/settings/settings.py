from dataclasses import dataclass
from typing import Final

from yaml import safe_load

from src.core.settings.app import AppSettings
from src.core.settings.cassandra import CassandraSettings


DEFAULT_SETTIGS_PATH: Final = 'config/config.yaml'


@dataclass(frozen=True)
class Settings:
    app: AppSettings
    cassandra: CassandraSettings

    @classmethod
    def load_from_yaml(cls, path_to_yaml: str = DEFAULT_SETTIGS_PATH) -> 'Settings':
        with open(path_to_yaml, 'r') as file:
            content = safe_load(file)

            return Settings(
                app=AppSettings(**content['app']),
                cassandra=CassandraSettings(**content['cassandra']),
            )


settings = Settings.load_from_yaml()
