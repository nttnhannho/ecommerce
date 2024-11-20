import asyncio

import pytest
from bson import ObjectId

from auth.auth_handler import Header, AuthHandler
from core.error_response import (
    StatusCode as ErrorStatusCode,
    ReasonStatusCode as ErrorReasonStatusCode,
)
from core.success_response import StatusCode as SuccessStatusCode, ReasonStatusCode as SuccessReasonStatusCode
from helpers.key_generator import KeyGenerator
from models.shop_model import Shop
from services.api_key_service import ApiKeyService
from services.key_token_service import KeyTokenService
from services.product_service import (
    ProductService,
    ClothingProductService,
    ElectronicProductService,
    FurnitureProductService,
)
from services.shop_service import ShopService
from tests.test_setup import test_client


@pytest.fixture
def setup_and_tear_down():
    asyncio.run(KeyTokenService.remove_all())
    asyncio.run(ApiKeyService.remove_all())
    asyncio.run(ProductService.remove_all())
    asyncio.run(ClothingProductService.remove_all())
    asyncio.run(ElectronicProductService.remove_all())
    asyncio.run(FurnitureProductService.remove_all())
    asyncio.run(ShopService.remove_all())

    asyncio.run(ApiKeyService.insert_one({'key': 'fake_key', 'permission': ['0000']}))
    shop_data = {
        '_id': ObjectId('673076a1e502936cad33841a'),
        'name': 'Shop A',
        'email': 'test@example.com',
        'password': '123456',
        'roles': ['SHOP'],
    }
    new_shop = Shop(**shop_data)
    asyncio.run(ShopService.insert_one(new_shop.model_dump(by_alias=True)))

    yield None

    asyncio.run(KeyTokenService.remove_all())
    asyncio.run(ApiKeyService.remove_all())
    asyncio.run(ProductService.remove_all())
    asyncio.run(ClothingProductService.remove_all())
    asyncio.run(ElectronicProductService.remove_all())
    asyncio.run(FurnitureProductService.remove_all())


def test_create_product(setup_and_tear_down):
    url = '/v1/api/products'
    data = {
        'name': 'Iphone 16',
        'description': 'New product',
        'price': 1000.00,
        'ptype': 'Electronic',
        'thumbnail': 'thumbnail',
        'quantity': 200,
        'attributes': {
            'manufacturer': 'Apple',
            'model': 'IP16',
            'color': 'Blue'
        }
    }

    shop_id = '673076a1e502936cad33841a'
    private_key = asyncio.run(KeyGenerator.generate_random_base64(length=64))
    public_key = asyncio.run(KeyGenerator.generate_random_base64(length=64))
    payload = {
        'id': shop_id,
        'email': 'test@example.com',
    }
    access_token, refresh_token = asyncio.run(AuthHandler.create_token_pair(
        payload=payload,
        public_key=public_key,
        private_key=private_key,
    ))
    asyncio.run(KeyTokenService.create_key_token(
        shop_id=ObjectId(shop_id),
        private_key=private_key,
        public_key=public_key,
        refresh_token=refresh_token,
    ))
    headers = {
        Header.API_KEY.value: 'fake_key',
        Header.CLIENT_ID.value: shop_id,
        Header.AUTHORIZATION.value: access_token,
    }

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == SuccessStatusCode.CREATED.value
    assert content['metadata']['_id']
    assert content['metadata']['shop_id'] == shop_id
    assert content['reason_status_code'] == SuccessReasonStatusCode.CREATED.value
    assert content['options']['limit'] == 10


def test_create_product_with_incorrect_product_type(setup_and_tear_down):
    url = '/v1/api/products'
    data = {
        'name': 'Iphone 16',
        'description': 'New product',
        'price': 1000.00,
        'ptype': 'Incorrect Product Type',
        'thumbnail': 'thumbnail',
        'quantity': 200,
        'attributes': {
            'manufacturer': 'Apple',
            'model': 'IP16',
            'color': 'Blue'
        }
    }

    shop_id = '673076a1e502936cad33841a'
    private_key = asyncio.run(KeyGenerator.generate_random_base64(length=64))
    public_key = asyncio.run(KeyGenerator.generate_random_base64(length=64))
    payload = {
        'id': shop_id,
        'email': 'test@example.com',
    }
    access_token, refresh_token = asyncio.run(AuthHandler.create_token_pair(
        payload=payload,
        public_key=public_key,
        private_key=private_key,
    ))
    asyncio.run(KeyTokenService.create_key_token(
        shop_id=ObjectId(shop_id),
        private_key=private_key,
        public_key=public_key,
        refresh_token=refresh_token,
    ))
    headers = {
        Header.API_KEY.value: 'fake_key',
        Header.CLIENT_ID.value: shop_id,
        Header.AUTHORIZATION.value: access_token,
    }

    response = test_client.post(url, headers=headers, json=data)
    content = response.json()

    assert response.status_code == ErrorStatusCode.BAD_REQUEST.value
    assert content['reason_status_code'] == ErrorReasonStatusCode.PRODUCT_TYPE_ERROR.value
