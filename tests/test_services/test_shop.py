import pytest
from starlette import status

from dbs.mongodb import mongodb
from models.api_key import ApiKey
from models.key_token_model import KeyToken
from models.shop_model import Shop
from tests.test_setup import test_client


@pytest.fixture
def collection():
    shop = mongodb[Shop.__collection_name__]
    api_key = mongodb[ApiKey.__collection_name__]
    api_key.insert_one({
        'key': 'fake_key',
        'permission': ['0000'],
    })

    yield shop

    shop.delete_many({})
    key_token = mongodb[KeyToken.__collection_name__]
    key_token.delete_many({})
    api_key.delete_many({})


def test_sign_up(collection):
    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop A',
        'email': 'test@example.com',
        'password': '123456',
        'roles': ['SHOP'],
    }
    headers = {'X-API-Key': 'fake_key'}

    response = test_client.post(url, headers=headers, json=data)

    assert response.status_code == status.HTTP_201_CREATED
    metadata = response.json()['metadata']
    assert metadata['shop']['_id']
    assert metadata['shop']['email'] == data['email']
    assert metadata['tokens']['access_token']
    assert metadata['tokens']['refresh_token']


def test_sign_up_with_missing_x_api_key_in_header(collection):
    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop A',
        'email': 'test@example.com',
        'password': '123456',
        'roles': ['SHOP'],
    }
    headers = {'Content-Type': 'application/json'}

    response = test_client.post(url, headers=headers, json=data)

    error_code = 'FORBIDDEN_ERROR'
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['code'] == error_code


def test_sign_up_with_incorrect_permission(collection):
    api_key_collection = mongodb[ApiKey.__collection_name__]
    api_key_collection.update_one(
        {'key': 'fake_key'},
        {'$set': {'permission': ['9999']}}
    )

    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop A',
        'email': 'test@example.com',
        'password': '123456',
        'roles': ['SHOP'],
    }
    headers = {'X-API-Key': 'fake_key'}

    response = test_client.post(url, headers=headers, json=data)

    error_code = 'PERMISSION_DENIED'
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()['code'] == error_code


def test_sign_up_with_request_is_missing_email(collection):
    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop A',
        'password': '123456',
    }
    headers = {'X-API-Key': 'fake_key'}

    response = test_client.post(url, headers=headers, json=data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_signup_with_existed_email_in_database(collection):
    collection.insert_one({
        'name': 'existed shop',
        'email': 'existed@example.com',
        'password': '123456',
    })

    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop B',
        'email': 'existed@example.com',
        'password': '123456',
    }
    headers = {'X-API-Key': 'fake_key'}

    response = test_client.post(url, headers=headers, json=data)

    error_code = 'EMAIL_IS_ALREADY_REGISTERED'
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == error_code
