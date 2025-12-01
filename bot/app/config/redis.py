from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RedisConfig:
    host: str
    port: int
    db: int
    password: str

    @classmethod
    def read_config(cls, redis: dict[str, Any]) -> 'RedisConfig':
        return cls(
            host=redis['host'],
            port=redis['port'],
            db=redis['db'],
            password=redis['password'],
        )
