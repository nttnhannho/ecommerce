import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

dev = {
    'db': {
        'host': os.getenv('DEV_DB_HOST'),
        'port': os.getenv('DEV_DB_PORT'),
    },
    'app': {
        'host': os.getenv('DEV_APP_HOST'),
        'port': os.getenv('DEV_APP_PORT'),
    },
}

test = {
    'db': {
        'host': os.getenv('TEST_DB_HOST'),
        'port': os.getenv('TEST_DB_PORT'),
    },
    'app': {
        'host': os.getenv('TEST_APP_HOST'),
        'port': os.getenv('TEST_APP_PORT'),
    },
}

prod = {
    'db': {
        'host': os.getenv('PROD_DB_HOST'),
        'port': os.getenv('PROD_DB_PORT'),
    },
    'app': {
        'host': os.getenv('PROD_APP_HOST'),
        'port': os.getenv('PROD_APP_PORT'),
    },
}


class EnvEnum(str, Enum):
    DEV = 'dev'
    TEST = 'test'
    PROD = 'prod'


cfg = {
    EnvEnum.DEV.value: dev,
    EnvEnum.TEST.value: test,
    EnvEnum.PROD.value: prod,
}
env = os.getenv('ENVIRONMENT') or 'dev'
env_config = cfg.get(env)
