from pymongo import MongoClient

from dbs.database import IDatabase
from exceptions.misc import MongoDBConnectionException, MongoDBDisconnectionException
from utils.env_configuration import env_config
from setting import IS_UNIT_TEST


class MongoDB(IDatabase):
    def __init__(self, connection_str):
        self.__con_str = connection_str
        self.__client = None
        self.connect()

    def __getitem__(self, item):
        return self.__client[item]

    def connect(self):
        try:
            self.__client = MongoClient(self.__con_str)
        except Exception:
            raise MongoDBConnectionException

    def disconnect(self):
        try:
            self.__client.close()
        except Exception:
            raise MongoDBDisconnectionException

    @staticmethod
    def get_instance():
        return MongoDB.__call__()


host = env_config['db']['host']
port = env_config['db']['port']
name = env_config['db']['name']
test_db = 'test_db'
connection_string = f'mongodb://{host}:{port}'
client = MongoDB(connection_string)
mongodb = client[name] if not IS_UNIT_TEST else client['test_db']
