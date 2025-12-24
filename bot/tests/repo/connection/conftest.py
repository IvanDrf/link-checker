import pytest

from app.config.config import AppConfig, Config, RabbitmqConfig, RedisConfig


@pytest.fixture(scope='session')
def config() -> Config:
    return Config(
        app=AppConfig(
            logger_level='debug',
            bot_token='',
            storage_path='storage/sqlite/test.db'
        ),
        rabbitmq=RabbitmqConfig(
            username='',
            password='',
            host='',
            port='',
            cons_queue='',
            produs_queue='',
        ),
        redis=RedisConfig('', 0, 0, ''))
