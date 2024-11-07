import pytest
from starlette import status

from core.error_response import (
    ForbiddenException,
    StatusCode as ErrorStatusCode,
    ReasonStatusCode as ErrorReasonStatusCode,
    PermissionDeniedException,
    BadRequestException,
)
from core.success_response import StatusCode as SuccessStatusCode, ReasonStatusCode as SuccessReasonStatusCode
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

    assert response.status_code == SuccessStatusCode.CREATED.value
    content = response.json()
    shop_id = content['metadata']['_id']
    assert shop_id
    assert content['metadata']['email'] == data['email']
    assert content['tokens']['access_token']
    assert content['tokens']['refresh_token']
    assert content['reason_status_code'] == SuccessReasonStatusCode.CREATED.value
    assert content['options']['limit'] == 10

    key_token = mongodb[KeyToken.__collection_name__]
    key_token_obj = key_token.find_one({'shop_id': shop_id})
    assert key_token_obj['private_key']
    assert key_token_obj['public_key']

    api_key = mongodb[ApiKey.__collection_name__]
    count = api_key.count_documents({})
    assert count == 2


def test_sign_up_with_missing_x_api_key_in_header(collection):
    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop A',
        'email': 'test@example.com',
        'password': '123456',
        'roles': ['SHOP'],
    }
    headers = {'Content-Type': 'application/json'}

    with pytest.raises(ForbiddenException) as exc:
        test_client.post(url, headers=headers, json=data)

    assert exc.value.status_code == ErrorStatusCode.FORBIDDEN.value
    assert exc.value.reason_status_code == ErrorReasonStatusCode.FORBIDDEN.value


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

    with pytest.raises(PermissionDeniedException) as exc:
        test_client.post(url, headers=headers, json=data)

    assert exc.value.status_code == ErrorStatusCode.PERMISSION_DENIED.value
    assert exc.value.reason_status_code == ErrorReasonStatusCode.PERMISSION_DENIED.value


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

    with pytest.raises(BadRequestException) as exc:
        test_client.post(url, headers=headers, json=data)

    assert exc.value.status_code == ErrorStatusCode.BAD_REQUEST.value
    assert exc.value.reason_status_code == ErrorReasonStatusCode.BAD_REQUEST.value
