from abc import ABC, abstractmethod

from helpers.singleton import SingletonMeta


class IDatabaseSingletonMeta(ABC, SingletonMeta):
    pass


class IDatabase(metaclass=IDatabaseSingletonMeta):
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def disconnect(self):
        ...
