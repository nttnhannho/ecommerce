from exceptions.custom import CustomException
from exceptions.message import (
    DEFAULT_SHOP_SERVICE_FIND_BY_EMAIL_EXCEPTION_MESSAGE,
    DEFAULT_SHOP_SERVICE_FIND_ONE_EXCEPTION_MESSAGE,
    DEFAULT_SHOP_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE,
    DEFAULT_SHOP_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE,
)


class ShopServiceFindByEmailException(CustomException):
    def __init__(self, message=DEFAULT_SHOP_SERVICE_FIND_BY_EMAIL_EXCEPTION_MESSAGE):
        super().__init__(message)


class ShopServiceFindOneException(CustomException):
    def __init__(self, message=DEFAULT_SHOP_SERVICE_FIND_ONE_EXCEPTION_MESSAGE):
        super().__init__(message)


class ShopServiceInsertOneException(CustomException):
    def __init__(self, message=DEFAULT_SHOP_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE):
        super().__init__(message)


class ShopServiceRemoveAllException(CustomException):
    def __init__(self, message=DEFAULT_SHOP_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE):
        super().__init__(message)
