from exceptions.custom import CustomException
from exceptions.message import (
    DEFAULT_PRODUCT_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE,
    DEFAULT_PRODUCT_SERVICE_CREATE_EXCEPTION_MESSAGE,
    DEFAULT_CLOTHING_PRODUCT_CREATE_EXCEPTION_MESSAGE,
    DEFAULT_ELECTRONIC_PRODUCT_CREATE_EXCEPTION_MESSAGE,
    DEFAULT_FURNITURE_PRODUCT_CREATE_EXCEPTION_MESSAGE,
    DEFAULT_CLOTHING_PRODUCT_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE,
    DEFAULT_ELECTRONIC_PRODUCT_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE,
    DEFAULT_FURNITURE_PRODUCT_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE,
    DEFAULT_PRODUCT_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE,
    DEFAULT_CLOTHING_PRODUCT_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE,
    DEFAULT_ELECTRONIC_PRODUCT_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE,
    DEFAULT_FURNITURE_PRODUCT_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE,
)


class ClothingProductCreateException(CustomException):
    def __init__(self, message=DEFAULT_CLOTHING_PRODUCT_CREATE_EXCEPTION_MESSAGE):
        super().__init__(message)


class ElectronicProductCreateException(CustomException):
    def __init__(self, message=DEFAULT_ELECTRONIC_PRODUCT_CREATE_EXCEPTION_MESSAGE):
        super().__init__(message)


class FurnitureProductCreateException(CustomException):
    def __init__(self, message=DEFAULT_FURNITURE_PRODUCT_CREATE_EXCEPTION_MESSAGE):
        super().__init__(message)


class ProductServiceInsertOneException(CustomException):
    def __init__(self, message=DEFAULT_PRODUCT_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE):
        super().__init__(message)


class ProductServiceRemoveAllException(CustomException):
    def __init__(self, message=DEFAULT_PRODUCT_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE):
        super().__init__(message)


class ClothingProductServiceRemoveAllException(CustomException):
    def __init__(self, message=DEFAULT_CLOTHING_PRODUCT_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE):
        super().__init__(message)


class ElectronicProductServiceRemoveAllException(CustomException):
    def __init__(self, message=DEFAULT_ELECTRONIC_PRODUCT_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE):
        super().__init__(message)


class FurnitureProductServiceRemoveAllException(CustomException):
    def __init__(self, message=DEFAULT_FURNITURE_PRODUCT_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE):
        super().__init__(message)


class ClothingProductServiceInsertOneException(CustomException):
    def __init__(self, message=DEFAULT_CLOTHING_PRODUCT_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE):
        super().__init__(message)


class ElectronicProductServiceInsertOneException(CustomException):
    def __init__(self, message=DEFAULT_ELECTRONIC_PRODUCT_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE):
        super().__init__(message)


class FurnitureProductServiceInsertOneException(CustomException):
    def __init__(self, message=DEFAULT_FURNITURE_PRODUCT_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE):
        super().__init__(message)


class ProductCreateException(CustomException):
    def __init__(self, message=DEFAULT_PRODUCT_SERVICE_CREATE_EXCEPTION_MESSAGE):
        super().__init__(message)
