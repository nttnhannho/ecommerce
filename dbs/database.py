from abc import ABC, abstractmethod


class IDatabase(ABC):
    @abstractmethod
    def connect(self):
        ...
