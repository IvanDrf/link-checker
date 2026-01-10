from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class DatabaseSettings:
    user: str
    password: Optional[str]

    host: str
    port: int
    db_name: str

    @property
    def dsn(self) -> str:
        if self.password is None:
            return f'postgresql+asyncpg://{self.user}@{self.host}:{self.port}/{self.db_name}'

        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'
