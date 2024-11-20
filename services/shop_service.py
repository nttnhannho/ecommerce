from bson import ObjectId

from auth.auth_handler import AuthHandler
from core.error_response import (
    BadRequestException,
    InternalServerError,
    UnauthorizedException,
    ReasonStatusCode as ErrorReasonStatusCode, ForbiddenException,
)
from core.success_response import (
    CreatedResponse,
    ReasonStatusCode as SuccessReasonStatusCode,
    SuccessResponse, NoContentResponse,
)
from dbs.mongodb import mongodb
from exceptions.shops.exception import (
    ShopServiceFindByEmailException,
    ShopServiceFindOneException,
    ShopServiceInsertOneException,
    ShopServiceRemoveAllException,
)
from helpers.hashing import Hash
from helpers.key_generator import KeyGenerator
from helpers.response_data_handler import ResponseDataHandler
from models.api_key_model import PermissionCode
from models.shop_model import Shop, ShopRole
from services.api_key_service import ApiKeyService
from services.key_token_service import KeyTokenService


class ShopService:
    collection = mongodb[Shop.__collection_name__]

    @staticmethod
    async def handle_token(request):
        """
        1 - check if refresh token in refresh token used list
        2 - check if refresh token is valid
        3 - check if shop is found by decoded shop email
        4 - create access token, refresh token
        5 - update key tokens and response success
        """
        decoded_shop = request.state.decoded_shop
        key_token_obj = request.state.key_token_obj
        refresh_token = request.state.refresh_token

        id_ = decoded_shop['id']
        email = decoded_shop['email']

        if refresh_token in key_token_obj['refresh_token_used']:
            await KeyTokenService.remove_by_shop_id(id_)
            raise ForbiddenException(detail=ErrorReasonStatusCode.RELOGIN_REQUIRED.value)

        if key_token_obj['refresh_token'] != refresh_token:
            raise UnauthorizedException(detail=ErrorReasonStatusCode.UNAUTHORIZED.value)

        found_shop = await ShopService.find_by_email(email)
        if not found_shop:
            raise UnauthorizedException(detail=ErrorReasonStatusCode.UNAUTHORIZED.value)

        payload = {'id': str(id_), 'email': email}
        new_access_token, new_refresh_token = await AuthHandler.create_token_pair(
            payload=payload,
            private_key=key_token_obj['private_key'],
            public_key=key_token_obj['public_key'],
        )

        filter_ = {'_id': ObjectId(key_token_obj['_id'])}
        update = {
            '$set': {'refresh_token': new_refresh_token},
            '$push': {'refresh_token_used': refresh_token}
        }
        await KeyTokenService.update_one(filter_, update)

        content = {
            'message': 'Handled token successfully',
            'reason_status_code': SuccessReasonStatusCode.SUCCESS.value,
            'metadata': await ResponseDataHandler.response_data(
                obj_dict=found_shop,
                fields=('_id', 'email'),
            ),
            'tokens': {
                'access_token': new_access_token,
                'refresh_token': new_refresh_token,
            },
            'options': {'limit': 10},
        }

        return SuccessResponse(content=content)

    @staticmethod
    async def log_out(request):
        """
        remove all key tokens related to logging out shop
        """
        await KeyTokenService.remove_by_id(request.state.key_token_id)
        return NoContentResponse()

    @staticmethod
    async def log_in(request):
        """
        1 - check if email is registered
        2 - check if password is matched
        3 - create private key, public key
        4 - create access token, refresh token
        """
        payload = await request.json()
        email = payload.get('email')
        password = payload.get('password')

        if not (email and password):
            raise BadRequestException(detail=ErrorReasonStatusCode.REQUEST_BODY_ERROR.value)

        found_shop = await ShopService.find_by_email(email=email)
        if not found_shop:
            raise BadRequestException(detail=ErrorReasonStatusCode.EMAIL_ERROR.value)

        is_password_matched = await Hash.is_password_matched(
            password=password,
            hashed_password=found_shop['password'],
        )
        if not is_password_matched:
            raise UnauthorizedException(detail=ErrorReasonStatusCode.UNAUTHORIZED.value)

        # For low level design
        private_key = await KeyGenerator.generate_random_base64(length=64)
        public_key = await KeyGenerator.generate_random_base64(length=64)

        shop_id = found_shop['_id']
        payload = {'id': str(shop_id), 'email': found_shop['email']}
        access_token, refresh_token = await AuthHandler.create_token_pair(
            payload=payload,
            private_key=private_key,
            public_key=public_key,
        )

        await KeyTokenService.create_key_token(
            shop_id=ObjectId(shop_id),
            private_key=private_key,
            public_key=public_key,
            refresh_token=refresh_token,
        )

        content = {
            'message': 'Login successfully',
            'reason_status_code': SuccessReasonStatusCode.SUCCESS.value,
            'metadata': await ResponseDataHandler.response_data(
                obj_dict=found_shop,
                fields=('_id', 'email'),
            ),
            'tokens': {
                'access_token': access_token,
                'refresh_token': refresh_token,
            },
            'options': {'limit': 10},
        }

        return SuccessResponse(content=content)

    @staticmethod
    async def sign_up(request):
        """
        1 - check if email is registered
        2 - hash password
        3 - create private key and public key
        4 - create access token and refresh token
        5 - create API key
        """
        payload = await request.json()
        name = payload.get('name')
        email = payload.get('email')
        password = payload.get('password')

        if not (name and email and password):
            raise BadRequestException(detail=ErrorReasonStatusCode.REQUEST_BODY_ERROR.value)

        existed_shop = await ShopService.find_by_email(email=email)
        if existed_shop:
            raise BadRequestException(detail=ErrorReasonStatusCode.EMAIL_ERROR.value)

        hashed_password = await Hash.hash_password(password=password)
        roles = [ShopRole.SHOP]
        shop_data = {
            'name': name,
            'email': email,
            'password': hashed_password,
            'roles': roles,
        }
        new_shop = Shop(**shop_data)

        if new_shop:
            # For high level design
            # private_key, public_key = await KeyGenerator.generate_rsa_keypair()
            # public_key_pem = await KeyGenerator.create_public_key_pem(public_key)

            # For low level design
            private_key = await KeyGenerator.generate_random_base64(length=64)
            public_key = await KeyGenerator.generate_random_base64(length=64)

            payload = {
                'id': str(new_shop.id),
                'email': new_shop.email,
            }
            access_token, refresh_token = await AuthHandler.create_token_pair(
                payload=payload,
                public_key=public_key,
                private_key=private_key,
            )

            key_token_dict = await KeyTokenService.create_key_token(
                shop_id=new_shop.id,
                private_key=private_key,
                public_key=public_key,
                refresh_token=refresh_token,
            )
            if not key_token_dict:
                return InternalServerError(detail=ErrorReasonStatusCode.KEY_TOKEN_ERROR.value)

            api_key = await KeyGenerator.generate_random_base64(length=64)
            permission = [PermissionCode.P0000.value]
            api_key_obj = await ApiKeyService.create_api_key(key=api_key, permission=permission)

            # Insert shop to DB
            new_shop_dict = new_shop.model_dump(by_alias=True)
            await ShopService.insert_one(new_shop_dict)

            # Insert API key to DB
            api_key_dict = api_key_obj.model_dump(by_alias=True)
            await ApiKeyService.insert_one(api_key_dict)

            content = {
                'message': 'Created new shop',
                'reason_status_code': SuccessReasonStatusCode.CREATED.value,
                'metadata': await ResponseDataHandler.response_data(
                    obj_dict=new_shop_dict,
                    fields=('_id', 'name', 'email'),
                ),
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                },
                'options': {'limit': 10},
            }

            return CreatedResponse(content=content)

    @staticmethod
    async def find_by_email(email):
        try:
            shop_obj = ShopService.collection.find_one({'email': email})
        except Exception:
            raise ShopServiceFindByEmailException

        return shop_obj

    @staticmethod
    async def find_one(data):
        try:
            shop_obj = ShopService.collection.find_one(data)
        except Exception:
            raise ShopServiceFindOneException

        return shop_obj

    @staticmethod
    async def insert_one(shop):
        try:
            ShopService.collection.insert_one(shop)
        except Exception:
            raise ShopServiceInsertOneException

    @staticmethod
    async def remove_all():
        try:
            ShopService.collection.delete_many({})
        except Exception:
            raise ShopServiceRemoveAllException
