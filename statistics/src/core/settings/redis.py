from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RedisSettings:
    host: str
    port: int
    database: int

    password: str
