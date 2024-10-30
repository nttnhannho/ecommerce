from exceptions.error_message import DEFAULT_MONGODB_CONNECTION_ERROR_MESSAGE


class CustomError(Exception):
    def __init__(self, message):
        self._message = message

    @property
    def message(self):
        return self._message

    def __str__(self):
        return f'{self._message}'


class MongoDBConnectionError(CustomError):
    def __init__(self, message=DEFAULT_MONGODB_CONNECTION_ERROR_MESSAGE):
        super().__init__(message)
