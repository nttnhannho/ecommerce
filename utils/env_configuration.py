import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

dev = {
    'db': {
        'host': os.getenv('DEV_DB_HOST'),
        'port': os.getenv('DEV_DB_PORT'),
        'name': os.getenv('DEV_DB_NAME'),
    },
    'app': {
        'host': os.getenv('DEV_APP_HOST'),
        'port': os.getenv('DEV_APP_PORT'),
        'reload': os.getenv('DEV_APP_RELOAD'),
        'workers': os.getenv('DEV_APP_WORKERS'),
    },
}

test = {
    'db': {
        'host': os.getenv('TEST_DB_HOST'),
        'port': os.getenv('TEST_DB_PORT'),
        'name': os.getenv('TEST_DB_NAME'),
    },
    'app': {
        'host': os.getenv('TEST_APP_HOST'),
        'port': os.getenv('TEST_APP_PORT'),
        'reload': os.getenv('TEST_APP_RELOAD'),
        'workers': os.getenv('TEST_APP_WORKERS'),
    },
}

prod = {
    'db': {
        'host': os.getenv('PROD_DB_HOST'),
        'port': os.getenv('PROD_DB_PORT'),
        'name': os.getenv('PROD_DB_NAME'),
    },
    'app': {
        'host': os.getenv('PROD_APP_HOST'),
        'port': os.getenv('PROD_APP_PORT'),
        'reload': os.getenv('PROD_APP_RELOAD'),
        'workers': os.getenv('PROD_APP_WORKERS'),
    },
}


class EnvEnum(str, Enum):
    DEV = 'dev'
    TEST = 'tests'
    PROD = 'prod'


cfg = {
    EnvEnum.DEV.value: dev,
    EnvEnum.TEST.value: test,
    EnvEnum.PROD.value: prod,
}
env = os.getenv('ENVIRONMENT') or 'dev'
env_config = cfg.get(env)
