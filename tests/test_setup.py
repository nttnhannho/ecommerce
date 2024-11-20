from starlette.testclient import TestClient

from app import app
from exceptions.misc import UnitTestInapplicableSetting
from setting import IS_UNIT_TEST

if not IS_UNIT_TEST:
    raise UnitTestInapplicableSetting

test_client = TestClient(app)
