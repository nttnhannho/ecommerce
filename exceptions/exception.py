from exceptions.custom import CustomException
from exceptions.message import (
    DEFAULT_MONGODB_CONNECTION_EXCEPTION_MESSAGE,
    DEFAULT_MONGODB_DISCONNECTION_EXCEPTION_MESSAGE,
    DEFAULT_HASH_PASSWORD_EXCEPTION_MESSAGE,
    DEFAULT_KEY_GENERATOR_GENERATE_RSA_KEYPAIR_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_CREATE_KEY_TOKEN_EXCEPTION_MESSAGE,
    DEFAULT_AUTH_HANDLER_CREATE_TOKEN_PAIR_EXCEPTION_MESSAGE,
    DEFAULT_KEY_GENERATOR_CREATE_PUBLIC_KEYS_PEM_EXCEPTION_MESSAGE,
    DEFAULT_KEY_GENERATOR_GENERATE_RANDOM_BASE64_EXCEPTION_MESSAGE,
    DEFAULT_API_KEY_SERVICE_CREATE_API_KEY_EXCEPTION_MESSAGE,
    DEFAULT_HASH_CHECK_MATCHED_EXCEPTION_MESSAGE,
    DEFAULT_UNIT_TEST_INAPPLICABLE_SETTING_EXCEPTION_MESSAGE,
    DEFAULT_API_KEY_SERVICE_FIND_BY_KEY_EXCEPTION_MESSAGE,
    DEFAULT_API_KEY_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE,
    DEFAULT_API_KEY_SERVICE_UPDATE_ONE_EXCEPTION_MESSAGE,
    DEFAULT_API_KEY_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE,
    DEFAULT_SHOP_SERVICE_FIND_BY_EMAIL_EXCEPTION_MESSAGE,
    DEFAULT_SHOP_SERVICE_FIND_ONE_EXCEPTION_MESSAGE,
    DEFAULT_SHOP_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE,
    DEFAULT_SHOP_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_FIND_ONE_AND_UPDATE_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_INSERT_ONE_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_FIND_BY_SHOP_ID_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_REMOVE_BY_ID_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_FIND_BY_REFRESH_TOKEN_USED_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_REMOVE_BY_SHOP_ID_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_FIND_BY_REFRESH_TOKEN_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_REMOVE_ALL_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_UPDATE_ONE_EXCEPTION_MESSAGE,
)


class MongoDBConnectionException(CustomException):
    def __init__(self, message=DEFAULT_MONGODB_CONNECTION_EXCEPTION_MESSAGE):
        super().__init__(message)


class ApiKeyServiceCreateApiKeyException(CustomException):
    def __init__(self, message=DEFAULT_API_KEY_SERVICE_CREATE_API_KEY_EXCEPTION_MESSAGE):
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


class MongoDBDisconnectionException(CustomException):
    def __init__(self, message=DEFAULT_MONGODB_DISCONNECTION_EXCEPTION_MESSAGE):
        super().__init__(message)


class HashPasswordException(CustomException):
    def __init__(self, message=DEFAULT_HASH_PASSWORD_EXCEPTION_MESSAGE):
        super().__init__(message)


class HashCheckMatchedException(CustomException):
    def __init__(self, message=DEFAULT_HASH_CHECK_MATCHED_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyGeneratorGenerateRSAKeypairException(CustomException):
    def __init__(self, message=DEFAULT_KEY_GENERATOR_GENERATE_RSA_KEYPAIR_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyGeneratorCreatePublicKeyPemException(CustomException):
    def __init__(self, message=DEFAULT_KEY_GENERATOR_CREATE_PUBLIC_KEYS_PEM_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyGeneratorGenerateRandomBase64Exception(CustomException):
    def __init__(self, message=DEFAULT_KEY_GENERATOR_GENERATE_RANDOM_BASE64_EXCEPTION_MESSAGE):
        super().__init__(message)


class AuthHandlerCreateTokenPairException(CustomException):
    def __init__(self, message=DEFAULT_AUTH_HANDLER_CREATE_TOKEN_PAIR_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyTokenServiceCreateKeyTokenException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_CREATE_KEY_TOKEN_EXCEPTION_MESSAGE):
        super().__init__(message)


class UnitTestInapplicableSetting(CustomException):
    def __init__(self, message=DEFAULT_UNIT_TEST_INAPPLICABLE_SETTING_EXCEPTION_MESSAGE):
        super().__init__(message)


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


class KeyTokenServiceUpdateOneException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_UPDATE_ONE_EXCEPTION_MESSAGE):
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
