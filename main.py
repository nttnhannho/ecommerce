import uvicorn
from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from dbs.mongodb import MongoDB
from utilities.env_configuration import env_config

allow_hosts = ['localhost', '127.0.0.1']
minimum_size_in_byte = 1000
compression_level = 5
host = env_config['app']['host']
port = int(env_config['app']['port'])

app = FastAPI()
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allow_hosts)
app.add_middleware(GZipMiddleware, minimum_size=minimum_size_in_byte, compresslevel=compression_level)

instance = MongoDB.get_instance()


@app.get('/')
async def root():
    return {'database': id(instance)}


def main():
    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    main()
