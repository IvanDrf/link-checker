from dataclasses import dataclass


@dataclass(frozen=True)
class RedisSettings:
    host: str
    port: int
    database: int

    password: str
