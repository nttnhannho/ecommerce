from exceptions.custom import CustomException
from exceptions.message import (
    DEFAULT_API_KEY_SERVICE_FIND_BY_KEY_EXCEPTION_MESSAGE,
    DEFAULT_API_KEY_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE,
    DEFAULT_API_KEY_SERVICE_UPDATE_ONE_EXCEPTION_MESSAGE,
    DEFAULT_API_KEY_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE,
    DEFAULT_API_KEY_SERVICE_CREATE_API_KEY_EXCEPTION_MESSAGE,
    DEFAULT_API_KEY_SERVICE_COUNT_DOCUMENTS_EXCEPTION_MESSAGE,
)


class ApiKeyServiceCreateApiKeyException(CustomException):
    def __init__(self, message=DEFAULT_API_KEY_SERVICE_CREATE_API_KEY_EXCEPTION_MESSAGE):
        super().__init__(message)


class ApiKeyServiceCountDocumentException(CustomException):
    def __init__(self, message=DEFAULT_API_KEY_SERVICE_COUNT_DOCUMENTS_EXCEPTION_MESSAGE):
        super().__init__(message)


class ApiKeyServiceFindByKeyException(CustomException):
    def __init__(self, message=DEFAULT_API_KEY_SERVICE_FIND_BY_KEY_EXCEPTION_MESSAGE):
        super().__init__(message)


class ApiKeyServiceInsertOneException(CustomException):
    def __init__(self, message=DEFAULT_API_KEY_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE):
        super().__init__(message)


class ApiKeyServiceUpdateOneException(CustomException):
    def __init__(self, message=DEFAULT_API_KEY_SERVICE_UPDATE_ONE_EXCEPTION_MESSAGE):
        super().__init__(message)


class ApiKeyServiceRemoveAllException(CustomException):
    def __init__(self, message=DEFAULT_API_KEY_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE):
        super().__init__(message)
