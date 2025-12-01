from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AppConfig:
    logger_level: str
    bot_token: str
    storage_path: str

    @classmethod
    def read_config(cls, data: dict[str, Any]) -> 'AppConfig':
        return cls(
            logger_level=data['logger_level'],
            bot_token=data['bot_token'],
            storage_path=data['storage_path']
        )
