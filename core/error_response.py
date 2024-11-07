from enum import Enum


class StatusCode(Enum):
    FORBIDDEN = 403
    BAD_REQUEST = 400
    INTERNAL_SERVER_ERROR = 500
    PERMISSION_DENIED = 403


class ReasonStatusCode(str, Enum):
    FORBIDDEN = 'FORBIDDEN_ERROR'
    BAD_REQUEST = 'BAD_REQUEST'
    INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
    PERMISSION_DENIED = 'PERMISSION_DENIED'


class CustomHTTPException(Exception):
    def __init__(self, status_code, reason_status_code, message=None):
        self._status_code = status_code
        self._reason_status_code = reason_status_code
        self._message = message

    @property
    def status_code(self):
        return self._status_code

    @property
    def reason_status_code(self):
        return self._reason_status_code

    @property
    def message(self):
        return self._message


class ForbiddenException(CustomHTTPException):
    def __init__(self, status_code=StatusCode.FORBIDDEN.value, reason_status_code=ReasonStatusCode.FORBIDDEN.value, message=None):
        super().__init__(status_code, reason_status_code, message)


class BadRequestException(CustomHTTPException):
    def __init__(self, status_code=StatusCode.BAD_REQUEST.value, reason_status_code=ReasonStatusCode.BAD_REQUEST.value, message=None):
        super().__init__(status_code, reason_status_code, message)


class InternalServerError(CustomHTTPException):
    def __init__(self, status_code=StatusCode.INTERNAL_SERVER_ERROR.value, reason_status_code=ReasonStatusCode.INTERNAL_SERVER_ERROR.value, message=None):
        super().__init__(status_code, reason_status_code, message)


class PermissionDeniedException(CustomHTTPException):
    def __init__(self, status_code=StatusCode.PERMISSION_DENIED.value, reason_status_code=ReasonStatusCode.PERMISSION_DENIED.value, message=None):
        super().__init__(status_code, reason_status_code, message)
