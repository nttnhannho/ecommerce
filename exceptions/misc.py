from exceptions.custom import CustomException
from exceptions.message import (
    DEFAULT_MONGODB_CONNECTION_EXCEPTION_MESSAGE,
    DEFAULT_MONGODB_DISCONNECTION_EXCEPTION_MESSAGE,
    DEFAULT_HASH_PASSWORD_EXCEPTION_MESSAGE,
    DEFAULT_KEY_GENERATOR_GENERATE_RSA_KEYPAIR_EXCEPTION_MESSAGE,
    DEFAULT_AUTH_HANDLER_CREATE_TOKEN_PAIR_EXCEPTION_MESSAGE,
    DEFAULT_KEY_GENERATOR_CREATE_PUBLIC_KEYS_PEM_EXCEPTION_MESSAGE,
    DEFAULT_KEY_GENERATOR_GENERATE_RANDOM_BASE64_EXCEPTION_MESSAGE,
    DEFAULT_HASH_CHECK_MATCHED_EXCEPTION_MESSAGE,
    DEFAULT_UNIT_TEST_INAPPLICABLE_SETTING_EXCEPTION_MESSAGE,
    DEFAULT_RESPONSE_DATA_HANDLER_EXCEPTION_MESSAGE,
)


class MongoDBConnectionException(CustomException):
    def __init__(self, message=DEFAULT_MONGODB_CONNECTION_EXCEPTION_MESSAGE):
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


class UnitTestInapplicableSetting(CustomException):
    def __init__(self, message=DEFAULT_UNIT_TEST_INAPPLICABLE_SETTING_EXCEPTION_MESSAGE):
        super().__init__(message)


class ResponseDataHandlerException(CustomException):
    def __init__(self, message=DEFAULT_RESPONSE_DATA_HANDLER_EXCEPTION_MESSAGE):
        super().__init__(message)
