import logging
from sys import stdout
from frozendict import frozendict

from app.config.config import Config


def configure_logger(cfg: Config) -> None:
    logging.basicConfig(
        level=select_logger_level(cfg.app.logger_level),
        stream=stdout
    )


type LoggerLevel = int | str

levels: frozendict[str, LoggerLevel] = frozendict(
    debug=logging.DEBUG,
    info=logging.INFO,
    warn=logging.WARN,
    error=logging.ERROR
)


def select_logger_level(level: str) -> LoggerLevel:
    return levels[level]
