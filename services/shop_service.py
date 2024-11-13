from bson import ObjectId

from auth.auth_handler import AuthHandler
from core.error_response import (
    BadRequestException,
    InternalServerError,
    UnauthorizedException,
    ReasonStatusCode as ErrorReasonStatusCode,
)
from core.success_response import (
    CreatedResponse,
    ReasonStatusCode as SuccessReasonStatusCode,
    SuccessResponse, NoContentResponse,
)
from dbs.mongodb import mongodb
from helpers.hashing import Hash
from helpers.key_generator import KeyGenerator
from helpers.response_data_handler import ResponseDataHandler
from models.api_key import ApiKey, PermissionCode
from models.shop_model import Shop, ShopRole, ShopLogin
from services.api_key_service import ApiKeyService
from services.key_token_service import KeyTokenService


class ShopService:
    @staticmethod
    async def log_out(request):
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
        request = await request.json()
        email = request.get('email')
        password = request.get('password')

        if not (email and password):
            raise BadRequestException(detail=ErrorReasonStatusCode.REQUEST_BODY_ERROR.value)

        collection = mongodb[ShopLogin.__collection_name__]
        found_shop = await ShopService.find_by_email(collection, email=email
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
        payload = {
            'id': str(shop_id),
            'email': found_shop['email'],
        }
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
                obj=found_shop,
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
    async def find_by_email(collection, email):
        shop_obj = collection.find_one({'email': email})
        return shop_obj

    @staticmethod
    async def sign_up(request):
        """
        1 - check if email is registered
        2 - hash password
        3 - create private key and public key
        4 - create access token and refresh token
        5 - create API key
        """
        request = await request.json()
        name = request.get('name')
        email = request.get('email')
        password = request.get('password')

        if not (name and email and password):
            raise BadRequestException(detail=ErrorReasonStatusCode.REQUEST_BODY_ERROR.value)

        collection = mongodb[Shop.__collection_name__]
        existed_shop = await ShopService.find_by_email(collection, email=email)
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
            collection.insert_one(new_shop_dict)

            # Insert API key to DB
            api_key_dict = api_key_obj.model_dump(by_alias=True)
            collection = mongodb[ApiKey.__collection_name__]
            collection.insert_one(api_key_dict)

            content = {
                'message': 'Created new shop',
                'reason_status_code': SuccessReasonStatusCode.CREATED.value,
                'metadata': await ResponseDataHandler.response_data(
                    obj=new_shop_dict,
                    fields=('_id', 'name', 'email'),
                ),
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                },
                'options': {'limit': 10},
            }

            return CreatedResponse(content=content)
