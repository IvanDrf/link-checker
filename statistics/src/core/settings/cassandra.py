from dataclasses import dataclass


@dataclass(frozen=True)
class CassandraSettings:
    host: str
    port: int
    key_space: str
