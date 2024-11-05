from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from routers.router import router

origins = ['localhost', '127.0.0.1']
minimum_size_in_byte = 1000
compression_level = 5

app = FastAPI()

app.add_middleware(TrustedHostMiddleware, allowed_hosts=origins)
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
app.add_middleware(GZipMiddleware, minimum_size=minimum_size_in_byte, compresslevel=compression_level)

app.include_router(router)
