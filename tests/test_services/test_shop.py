import pytest
from starlette import status

from dbs.mongodb import mongodb
from models.key_token_model import KeyToken
from models.shop_model import Shop
from tests.test_setup import test_client


@pytest.fixture
def collection():
    collection = mongodb[Shop.__collection_name__]

    yield collection

    collection.delete_many({})
    key_token_collection = mongodb[KeyToken.__collection_name__]
    key_token_collection.delete_many({})


def test_sign_up(collection):
    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop A',
        'email': 'test@example.com',
        'password': '123456',
    }

    response = test_client.post(url, json=data)

    assert response.status_code == status.HTTP_201_CREATED
    metadata = response.json()['metadata']
    assert metadata['shop']['_id']
    assert metadata['shop']['email'] == data['email']
    assert metadata['tokens']['access_token']
    assert metadata['tokens']['refresh_token']


def test_sign_up_with_request_is_missing_email(collection):
    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop A',
        'password': '123456',
    }

    response = test_client.post(url, json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_signup_with_existed_email_in_database(collection):
    collection.insert_one({
        'name': 'Shop A',
        'email': 'test@example.com',
        'password': '123456',
    })

    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop B',
        'email': 'test@example.com',
        'password': '123456',
    }
    error_code = 'EMAIL_IS_ALREADY_REGISTERED'

    response = test_client.post(url, json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['code'] == error_code
