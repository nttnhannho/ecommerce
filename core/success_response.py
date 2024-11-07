from enum import Enum

from starlette.responses import JSONResponse


class StatusCode(Enum):
    CREATED = 201


class ReasonStatusCode(str, Enum):
    CREATED = 'CREATED'


class CustomSuccessResponse(JSONResponse):
    def __init__(self, content: dict, status_code):
        super().__init__(content, status_code)


class CreatedResponse(CustomSuccessResponse):
    def __init__(self, content: dict, status_code=StatusCode.CREATED.value):
        super().__init__(content, status_code)
