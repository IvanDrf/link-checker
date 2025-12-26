from dataclasses import dataclass


@dataclass(frozen=True)
class AppSettings:
    host: str
    port: str
