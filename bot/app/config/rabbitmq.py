from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RabbitmqConfig:
    username: str
    password: str
    host: str
    port: str
    cons_queue: str
    produs_queue: str

    @classmethod
    def read_config(cls, rabbit: dict[str, Any]) -> 'RabbitmqConfig':
        return cls(
            username=rabbit['username'],
            password=rabbit['password'],
            host=rabbit['host'],
            port=rabbit['port'],
            cons_queue=rabbit['consumer_queue'],
            produs_queue=rabbit['producer_queue']
        )
