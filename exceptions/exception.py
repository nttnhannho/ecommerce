from exceptions.custom import CustomException
from exceptions.message import (
    DEFAULT_MONGODB_CONNECTION_EXCEPTION_MESSAGE,
    DEFAULT_MONGODB_DISCONNECTION_EXCEPTION_MESSAGE,
    DEFAULT_HASH_BCRYPT_EXCEPTION_MESSAGE,
    DEFAULT_KEY_GENERATOR_GENERATE_RSA_KEYPAIR_EXCEPTION_MESSAGE,
    DEFAULT_KEY_TOKEN_SERVICE_CREATE_KEY_TOKEN_EXCEPTION_MESSAGE,
    DEFAULT_AUTH_HANDLER_CREATE_TOKEN_PAIR_EXCEPTION_MESSAGE,
    DEFAULT_KEY_GENERATOR_CREATE_PUBLIC_KEYS_PEM_EXCEPTION_MESSAGE,
)


class MongoDBConnectionException(CustomException):
    def __init__(self, message=DEFAULT_MONGODB_CONNECTION_EXCEPTION_MESSAGE):
        super().__init__(message)


class MongoDBDisconnectionException(CustomException):
    def __init__(self, message=DEFAULT_MONGODB_DISCONNECTION_EXCEPTION_MESSAGE):
        super().__init__(message)


class HashBcryptException(CustomException):
    def __init__(self, message=DEFAULT_HASH_BCRYPT_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyGeneratorGenerateRSAKeypairException(CustomException):
    def __init__(self, message=DEFAULT_KEY_GENERATOR_GENERATE_RSA_KEYPAIR_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyGeneratorCreatePublicKeyPemException(CustomException):
    def __init__(self, message=DEFAULT_KEY_GENERATOR_CREATE_PUBLIC_KEYS_PEM_EXCEPTION_MESSAGE):
        super().__init__(message)


class AuthHandlerCreateTokenPairException(CustomException):
    def __init__(self, message=DEFAULT_AUTH_HANDLER_CREATE_TOKEN_PAIR_EXCEPTION_MESSAGE):
        super().__init__(message)


class KeyTokenServiceCreateKeyTokenException(CustomException):
    def __init__(self, message=DEFAULT_KEY_TOKEN_SERVICE_CREATE_KEY_TOKEN_EXCEPTION_MESSAGE):
        super().__init__(message)
