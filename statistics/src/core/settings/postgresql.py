from dataclasses import dataclass


@dataclass(frozen=True)
class DatabaseSettings:
    user: str
    password: str

    host: str
    port: int
    db_name: str
