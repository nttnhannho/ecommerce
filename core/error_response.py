from enum import Enum

from starlette.exceptions import HTTPException


class StatusCode(Enum):
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    PERMISSION_DENIED = 403
    NOT_FOUND = 404


class ReasonStatusCode(str, Enum):
    BAD_REQUEST = 'BAD_REQUEST'
    INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
    UNAUTHORIZED = 'UNAUTHORIZED'
    FORBIDDEN = 'FORBIDDEN_ERROR'
    PERMISSION_DENIED = 'PERMISSION_DENIED'
    NOT_FOUND = 'NOT_FOUND'

    EMAIL_ERROR = 'EMAIL_ERROR'
    API_KEY_ERROR = 'API_KEY_ERROR'
    KEY_TOKEN_ERROR = 'KEY_TOKEN_ERROR'
    CLIENT_ID_ERROR = 'CLIENT_ID_ERROR'
    AUTHENTICATION_ERROR = 'ACCESS_TOKEN_ERROR'
    REQUEST_BODY_ERROR = 'REQUEST_BODY_ERROR'
    RELOGIN_REQUIRED = 'RELOGIN_REQUIRED'
    REFRESH_TOKEN_ERROR = 'REFRESH_TOKEN_ERROR'
    PRODUCT_TYPE_ERROR = 'PRODUCT_TYPE_ERROR'


class CustomErrorResponse(HTTPException):
    def __init__(self, status_code, detail):
        super().__init__(status_code, detail)


class BadRequestException(CustomErrorResponse):
    def __init__(self, status_code=StatusCode.BAD_REQUEST.value, detail=None):
        super().__init__(status_code, detail)


class NotFoundException(CustomErrorResponse):
    def __init__(self, status_code=StatusCode.NOT_FOUND.value, detail=None):
        super().__init__(status_code, detail)


class UnauthorizedException(CustomErrorResponse):
    def __init__(self, status_code=StatusCode.UNAUTHORIZED.value, detail=None):
        super().__init__(status_code, detail)


class InternalServerError(CustomErrorResponse):
    def __init__(self, status_code=StatusCode.INTERNAL_SERVER_ERROR.value, detail=None):
        super().__init__(status_code, detail)


class ForbiddenException(CustomErrorResponse):
    def __init__(self, status_code=StatusCode.FORBIDDEN.value, detail=None):
        super().__init__(status_code, detail)


class PermissionDeniedException(CustomErrorResponse):
    def __init__(self, status_code=StatusCode.PERMISSION_DENIED.value, detail=None):
        super().__init__(status_code, detail)
