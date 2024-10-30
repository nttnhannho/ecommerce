from fastapi import FastAPI

from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

allow_hosts = ['localhost', '127.0.0.1']
minimum_size_in_byte = 1000
compression_level = 5

app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allow_hosts)
app.add_middleware(GZipMiddleware, minimum_size=minimum_size_in_byte, compresslevel=compression_level)


@app.get('/')
async def root():
    return {'message': 'Hello World'}
