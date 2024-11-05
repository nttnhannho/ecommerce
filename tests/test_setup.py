from fastapi import FastAPI
from starlette.testclient import TestClient

from routers.router import router

test_app = FastAPI()
test_app.include_router(router)

test_client = TestClient(test_app)
