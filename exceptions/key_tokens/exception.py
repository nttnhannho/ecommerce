from exceptions.custom import CustomException
from exceptions.message import (
    DEFAULT_KEY_TOKEN_SERVICE_CREATE_KEY_TOKEN_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_UPDATE_ONE_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_FIND_ONE_AND_UPDATE_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_FIND_BY_SHOP_ID_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_REMOVE_BY_ID_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_FIND_BY_REFRESH_TOKEN_USED_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_REMOVE_BY_SHOP_ID_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_FIND_BY_REFRESH_TOKEN_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_FIND_ONE_EXCEPTION_MESSAGE,
)


class KeyTokenServiceCreateKeyTokenException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_CREATE_KEY_TOKEN_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyTokenServiceUpdateOneException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_UPDATE_ONE_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyTokenServiceFindOneException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_FIND_ONE_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyTokenServiceFindOneAndUpdateException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_FIND_ONE_AND_UPDATE_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyTokenServiceInsertOneException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyTokenServiceFindByShopIdException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_FIND_BY_SHOP_ID_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyTokenServiceRemoveByIdException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_REMOVE_BY_ID_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyTokenServiceFindByRefreshTokenUsedException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_FIND_BY_REFRESH_TOKEN_USED_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyTokenServiceRemoveByShopIdException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_REMOVE_BY_SHOP_ID_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyTokenServiceFindByRefreshTokenException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_FIND_BY_REFRESH_TOKEN_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyTokenServiceRemoveAllException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE):
        super().__init__(message)
