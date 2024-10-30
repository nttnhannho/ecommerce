from pymongo import MongoClient

from dbs.database import IDatabase
from exceptions.db_exception import MongoDBConnectionError
from helpers.singleton import SingletonMeta


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


connection_string = 'mongodb://localhost:27017'
mongodb = MongoDB(connection_string)
