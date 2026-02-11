import logging
from enum import Enum

from src.core.settings.settings import settings


def setup_logger() -> None:
    logging.basicConfig(
        level=__select_logger_level(),
        format='%(asctime)s %(levelname)s %(message)s'
    )


class LoggerLevel(Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARN = 'warn'
    ERROR = 'error'


def __select_logger_level() -> int:
    levels = {
        LoggerLevel.DEBUG.value: logging.DEBUG,
        LoggerLevel.INFO.value: logging.INFO,
        LoggerLevel.WARN.value: logging.WARN,
        LoggerLevel.ERROR.value: logging.ERROR
    }

    return levels[settings.app.logger_level]
