import asyncio

import pytest
from bson import ObjectId

from auth.auth_handler import Header, AuthHandler
from core.error_response import (
    StatusCode as ErrorStatusCode,
    ReasonStatusCode as ErrorReasonStatusCode,
)
from core.success_response import StatusCode as SuccessStatusCode, ReasonStatusCode as SuccessReasonStatusCode
from dbs.mongodb import mongodb
from helpers.hashing import Hash
from helpers.key_generator import KeyGenerator
from models.api_key import ApiKey
from models.key_token_model import KeyToken
from services.api_key_service import ApiKeyService
from services.key_token_service import KeyTokenService
from services.shop_service import ShopService
from tests.test_setup import test_client


@pytest.fixture
def setup_and_tear_down():
    asyncio.run(ApiKeyService.insert_one({'key': 'fake_key', 'permission': ['0000']}))

    yield None

    asyncio.run(ShopService.remove_all())
    asyncio.run(KeyTokenService.remove_all())
    asyncio.run(ApiKeyService.remove_all())


def test_sign_up(setup_and_tear_down):
    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop A',
        'email': 'test@example.com',
        'password': '123456',
        'roles': ['SHOP'],
    }
    headers = {Header.API_KEY.value: 'fake_key'}

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == SuccessStatusCode.CREATED.value
    shop_id = content['metadata']['_id']
    assert shop_id
    assert content['metadata']['email'] == data['email']
    assert content['tokens']['access_token']
    assert content['tokens']['refresh_token']
    assert content['reason_status_code'] == SuccessReasonStatusCode.CREATED.value
    assert content['options']['limit'] == 10

    key_token = mongodb[KeyToken.__collection_name__]
    key_token_obj = key_token.find_one({'shop_id': ObjectId(shop_id)})
    assert key_token_obj['private_key']
    assert key_token_obj['public_key']

    api_key = mongodb[ApiKey.__collection_name__]
    count = api_key.count_documents({})
    assert count == 2


def test_sign_up_with_missing_api_key_in_header(setup_and_tear_down):
    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop A',
        'email': 'test@example.com',
        'password': '123456',
        'roles': ['SHOP'],
    }
    headers = {'Content-Type': 'application/json'}

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == ErrorStatusCode.BAD_REQUEST.value
    assert content['reason_status_code'] == ErrorReasonStatusCode.API_KEY_ERROR.value


def test_sign_up_with_incorrect_api_key(setup_and_tear_down):
    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop A',
        'email': 'test@example.com',
        'password': '123456',
        'roles': ['SHOP'],
    }
    headers = {Header.API_KEY.value: 'incorrect_api_key'}

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == ErrorStatusCode.FORBIDDEN.value
    assert content['reason_status_code'] == ErrorReasonStatusCode.FORBIDDEN.value


def test_sign_up_with_incorrect_permission(setup_and_tear_down):
    filter_ = {'key': 'fake_key'}
    update_fields = {'$set': {'permission': ['9999']}}
    asyncio.run(ApiKeyService.update_one(filter_, update_fields))

    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop A',
        'email': 'test@example.com',
        'password': '123456',
        'roles': ['SHOP'],
    }
    headers = {Header.API_KEY.value: 'fake_key'}

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == ErrorStatusCode.PERMISSION_DENIED.value
    assert content['reason_status_code'] == ErrorReasonStatusCode.PERMISSION_DENIED.value


def test_sign_up_with_request_is_missing_email(setup_and_tear_down):
    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop A',
        'password': '123456',
    }
    headers = {Header.API_KEY.value: 'fake_key'}

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == ErrorStatusCode.BAD_REQUEST.value
    assert content['reason_status_code'] == ErrorReasonStatusCode.REQUEST_BODY_ERROR.value


def test_signup_with_registered_email(setup_and_tear_down):
    asyncio.run(ShopService.insert_one({
        'name': 'existed shop',
        'email': 'existed@example.com',
        'password': '123456',
    }))

    url = '/v1/api/shops/signup'
    data = {
        'name': 'Shop B',
        'email': 'existed@example.com',
        'password': '123456',
    }
    headers = {Header.API_KEY.value: 'fake_key'}

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == ErrorStatusCode.BAD_REQUEST.value
    assert content['reason_status_code'] == ErrorReasonStatusCode.EMAIL_ERROR.value


def test_login(setup_and_tear_down):
    password = '123456'
    hashed_password = asyncio.run(Hash.hash_password(password)).decode('utf-8')
    asyncio.run(ShopService.insert_one({
        'name': 'created shop',
        'email': 'created_shop@example.com',
        'password': hashed_password,
    }))

    url = '/v1/api/shops/login'
    data = {
        'email': 'created_shop@example.com',
        'password': '123456'
    }
    headers = {Header.API_KEY.value: 'fake_key'}

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == SuccessStatusCode.SUCCESS.value
    assert content['reason_status_code'] == SuccessReasonStatusCode.SUCCESS.value
    assert content['metadata']['email'] == data['email']
    assert content['tokens']['access_token']
    assert content['tokens']['refresh_token']
    assert content['options']['limit'] == 10


def test_login_with_request_is_missing_email(setup_and_tear_down):
    url = '/v1/api/shops/login'
    data = {
        'password': '123456'
    }
    headers = {Header.API_KEY.value: 'fake_key'}

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == ErrorStatusCode.BAD_REQUEST.value
    assert content['reason_status_code'] == ErrorReasonStatusCode.REQUEST_BODY_ERROR.value


def test_login_with_unregistered_shop(setup_and_tear_down):
    url = '/v1/api/shops/login'
    data = {
        'email': 'unregistered_shop@example.com',
        'password': '123456'
    }
    headers = {Header.API_KEY.value: 'fake_key'}

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == ErrorStatusCode.BAD_REQUEST.value
    assert content['reason_status_code'] == ErrorReasonStatusCode.EMAIL_ERROR.value


def test_login_with_incorrect_password(setup_and_tear_down):
    password = '123456'
    hashed_password = asyncio.run(Hash.hash_password(password)).decode('utf-8')
    asyncio.run(ShopService.insert_one({
        'name': 'created shop',
        'email': 'created_shop@example.com',
        'password': hashed_password,
    }))

    url = '/v1/api/shops/login'
    data = {
        'email': 'created_shop@example.com',
        'password': 'wrong password'
    }
    headers = {Header.API_KEY.value: 'fake_key'}

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == ErrorStatusCode.UNAUTHORIZED.value
    assert content['reason_status_code'] == ErrorReasonStatusCode.UNAUTHORIZED.value


def test_logout(setup_and_tear_down):
    asyncio.run(ShopService.insert_one({
        'name': 'created shop',
        'email': 'created_shop@example.com',
        'password': '123456',
    }))

    shop_obj = asyncio.run(ShopService.find_one({'email': 'created_shop@example.com'}))
    shop_id = str(shop_obj['_id'])
    shop_email = shop_obj['email']
    private_key = asyncio.run(KeyGenerator.generate_random_base64(length=64))
    public_key = asyncio.run(KeyGenerator.generate_random_base64(length=64))
    payload = {
        'id': shop_id,
        'email': shop_email,
    }
    access_token, refresh_token = asyncio.run(AuthHandler.create_token_pair(
        payload=payload,
        public_key=public_key,
        private_key=private_key,
    ))

    key_token = mongodb[KeyToken.__collection_name__]
    key_token.insert_one({
        'shop_id': ObjectId(shop_id),
        'private_key': private_key,
        'public_key': public_key,
        'refresh_token': refresh_token,
        'refresh_token_used': [],
    })

    url = '/v1/api/shops/logout'
    data = {}
    headers = {
        Header.API_KEY.value: 'fake_key',
        Header.CLIENT_ID.value: shop_id,
        Header.AUTHORIZATION.value: access_token,
    }

    response = test_client.post(url, headers=headers, json=data)

    assert response.status_code == SuccessStatusCode.NO_CONTENT.value


def test_logout_with_request_is_missing_api_key_in_header(setup_and_tear_down):
    url = '/v1/api/shops/logout'
    data = {}
    headers = {
        Header.CLIENT_ID.value: '67356e2b7f6df2c250f667ab',
        Header.AUTHORIZATION.value: 'access_token',
    }

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == ErrorStatusCode.BAD_REQUEST.value
    assert content['reason_status_code'] == ErrorReasonStatusCode.API_KEY_ERROR.value


def test_logout_with_request_is_missing_client_id_in_header(setup_and_tear_down):
    url = '/v1/api/shops/logout'
    data = {}
    headers = {
        Header.API_KEY.value: 'fake_key',
        Header.AUTHORIZATION.value: 'access_token',
    }

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == ErrorStatusCode.BAD_REQUEST.value
    assert content['reason_status_code'] == ErrorReasonStatusCode.CLIENT_ID_ERROR.value


def test_logout_with_request_is_missing_authorization_in_header(setup_and_tear_down):
    url = '/v1/api/shops/logout'
    data = {}
    headers = {
        Header.API_KEY.value: 'fake_key',
        Header.CLIENT_ID.value: '67356e2b7f6df2c250f667ab',
    }

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == ErrorStatusCode.BAD_REQUEST.value
    assert content['reason_status_code'] == ErrorReasonStatusCode.AUTHENTICATION_ERROR.value


def test_handle_token(setup_and_tear_down):
    asyncio.run(ShopService.insert_one({
        'name': 'created shop',
        'email': 'created_shop@example.com',
        'password': '123456',
    }))

    shop_obj = asyncio.run(ShopService.find_one({'email': 'created_shop@example.com'}))
    shop_id = str(shop_obj['_id'])
    shop_email = shop_obj['email']
    private_key = asyncio.run(KeyGenerator.generate_random_base64(length=64))
    public_key = asyncio.run(KeyGenerator.generate_random_base64(length=64))
    payload = {
        'id': shop_id,
        'email': shop_email,
    }
    access_token, refresh_token = asyncio.run(AuthHandler.create_token_pair(
        payload=payload,
        public_key=public_key,
        private_key=private_key,
    ))

    key_token = mongodb[KeyToken.__collection_name__]
    key_token.insert_one({
        'shop_id': ObjectId(shop_id),
        'private_key': private_key,
        'public_key': public_key,
        'refresh_token': refresh_token,
        'refresh_token_used': [],
    })

    url = '/v1/api/shops/handle-token'
    data = {}
    headers = {
        Header.API_KEY.value: 'fake_key',
        Header.CLIENT_ID.value: shop_id,
        Header.REFRESH_TOKEN.value: refresh_token
    }

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == SuccessStatusCode.SUCCESS.value
    assert content['reason_status_code'] == SuccessReasonStatusCode.SUCCESS.value
    assert content['metadata']['email'] == shop_email
    assert content['tokens']['access_token'] != access_token
    assert content['tokens']['refresh_token'] != refresh_token
    assert key_token.find_one({'refresh_token_used': {'$size': 1}})
    assert content['options']['limit'] == 10


def test_handle_token_with_request_is_missing_refresh_token_in_header(setup_and_tear_down):
    url = '/v1/api/shops/handle-token'
    data = {}
    headers = {
        Header.API_KEY.value: 'fake_key',
        Header.CLIENT_ID.value: '67356e2b7f6df2c250f667ab',
    }

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == ErrorStatusCode.BAD_REQUEST.value
    assert content['reason_status_code'] == ErrorReasonStatusCode.REFRESH_TOKEN_ERROR.value
