from starlette.testclient import TestClient

from app import app

test_client = TestClient(app)
