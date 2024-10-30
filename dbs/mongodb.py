from pymongo import MongoClient

from dbs.database import IDatabase
from exceptions.db_exception import MongoDBConnectionError
from helpers.singleton import SingletonMeta
from utilities.env_configuration import env_config


class MongoDBMeta(IDatabase, SingletonMeta):
    def connect(self):
        ...


class MongoDB(metaclass=MongoDBMeta):
    def __init__(self, connection_str):
        self.__con_str = connection_str
        self.__client = None
        self.connect()

    def connect(self):
        try:
            with MongoClient(self.__con_str) as client:
                self.__client = client
        except Exception:
            raise MongoDBConnectionError

    @staticmethod
    def get_instance():
        return MongoDB.__call__()


host = env_config['db']['host']
port = env_config['db']['port']
connection_string = f'mongodb://{host}:{port}'
mongodb = MongoDB(connection_string)
