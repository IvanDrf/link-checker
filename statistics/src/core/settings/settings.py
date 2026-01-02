from dataclasses import dataclass
from typing import Final

from yaml import safe_load

from src.core.settings.app import AppSettings
from src.core.settings.postgresql import DatabaseSettings


DEFAULT_SETTIGS_PATH: Final = 'config/config.yaml'


@dataclass(frozen=True)
class Settings:
    app: AppSettings
    database: DatabaseSettings

    @classmethod
    def load_from_yaml(cls, path_to_yaml: str = DEFAULT_SETTIGS_PATH) -> 'Settings':
        with open(path_to_yaml, 'r') as file:
            content = safe_load(file)

            return Settings(
                app=AppSettings(**content['app']),
                database=DatabaseSettings(**content['database']),
            )


settings = Settings.load_from_yaml()
