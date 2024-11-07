from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from routers.router import router
from services.api_key_service import ApiKeyService
from utils.setting import IS_UNIT_TEST

origins = ['localhost', '127.0.0.1'] if not IS_UNIT_TEST else ['testserver']
minimum_size_in_byte = 1000
compression_level = 5

app = FastAPI()


@app.middleware('http')
async def check_permission(request: Request, call_next, permission='0000'):
    api_key_obj = request.state.api_key_obj
    if permission not in api_key_obj['permission']:
        content = {
            'message': 'Permission Denied',
            'code': 'PERMISSION_DENIED',
        }
        return JSONResponse(content=content, status_code=status.HTTP_403_FORBIDDEN)

    response = await call_next(request)
    return response


@app.middleware('http')
async def check_api_key(request: Request, call_next):
    api_key = request.headers.get('X-API-Key')
    api_key_obj = ApiKeyService.find_by_key(key=api_key)
    if not (api_key and api_key_obj):
        content = {
            'message': 'Forbidden Error',
            'code': 'FORBIDDEN_ERROR',
        }
        return JSONResponse(content=content, status_code=status.HTTP_403_FORBIDDEN)

    request.state.api_key_obj = api_key_obj
    response = await call_next(request)
    return response


app.add_middleware(TrustedHostMiddleware, allowed_hosts=origins)
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.add_middleware(GZipMiddleware, minimum_size=minimum_size_in_byte, compresslevel=compression_level)

app.include_router(router)
