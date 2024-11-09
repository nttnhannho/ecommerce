from enum import Enum

from starlette.responses import JSONResponse


class StatusCode(Enum):
    CREATED = 201
    SUCCESS = 200


class ReasonStatusCode(str, Enum):
    CREATED = 'CREATED'
    SUCCESS = 'SUCCESS'


class CustomSuccessResponse(JSONResponse):
    def __init__(self, content: dict, status_code):
        super().__init__(content, status_code)


class CreatedResponse(CustomSuccessResponse):
    def __init__(self, content, status_code=StatusCode.CREATED.value):
        super().__init__(content, status_code)


class SuccessResponse(CustomSuccessResponse):
    def __init__(self, content, status_code=StatusCode.SUCCESS.value):
        super().__init__(content, status_code)
