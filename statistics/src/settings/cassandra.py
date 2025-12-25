from dataclasses import dataclass


@dataclass(frozen=True)
class CassandraSettings:
    host: str
    port: int
    name: str
