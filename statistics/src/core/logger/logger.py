import logging

from src.core.settings.settings import settings


def setup_logger() -> None:
    logging.basicConfig(level=_select_logger_level(),
                        format='%(asctime)s %(levelname)s %(message)s')


def _select_logger_level():
    levels = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARN,
        'error': logging.ERROR
    }

    return levels[settings.app.logger_level]
