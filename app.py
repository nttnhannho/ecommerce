from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from auth.auth_handler import Header
from core.error_response import (
    BadRequestException,
    ForbiddenException,
    PermissionDeniedException, ReasonStatusCode,
)
from routers.router import router
from services.api_key_service import ApiKeyService
from setting import IS_UNIT_TEST

origins = ['localhost', '127.0.0.1'] if not IS_UNIT_TEST else ['testserver']
minimum_size_in_byte = 1000
compression_level = 5

app = FastAPI()


@app.middleware('http')
async def check_permission(request: Request, call_next, permission=Header.DEFAULT_PERMISSION.value):
    api_key_obj = request.state.api_key_obj
    if permission not in api_key_obj['permission']:
        raise PermissionDeniedException(detail=ReasonStatusCode.PERMISSION_DENIED.value)

    response = await call_next(request)
    return response


@app.middleware('http')
async def check_api_key(request: Request, call_next):
    api_key = request.headers.get(Header.API_KEY.value)
    if not api_key:
        raise BadRequestException(detail=ReasonStatusCode.API_KEY_ERROR.value)

    api_key_obj = await ApiKeyService.find_by_key(key=api_key)
    if not api_key_obj:
        raise ForbiddenException(detail=ReasonStatusCode.FORBIDDEN.value)

    request.state.api_key_obj = api_key_obj

    response = await call_next(request)
    return response


@app.exception_handler(HTTPException)
async def handle_exception(request, exc):
    response = JSONResponse(status_code=exc.status_code, content={'reason_status_code': exc.detail})
    return response


class MiddlewareExceptionHandler(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except HTTPException as exc:
            return await handle_exception(request, exc)

        return response


app.add_middleware(TrustedHostMiddleware, allowed_hosts=origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(GZipMiddleware, minimum_size=minimum_size_in_byte, compresslevel=compression_level)
app.add_middleware(MiddlewareExceptionHandler)

app.include_router(router)
