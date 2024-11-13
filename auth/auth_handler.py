from datetime import datetime, timedelta
from enum import Enum

import jwt
from starlette.requests import Request

from core.error_response import ReasonStatusCode, NotFoundException, BadRequestException, UnauthorizedException
from exceptions.exception import AuthHandlerCreateTokenPairException
from services.key_token_service import KeyTokenService


class Header(str, Enum):
    API_KEY = 'x-api-key'
    CLIENT_ID = 'x-client-id'
    AUTHORIZATION = 'authorization'
    DEFAULT_PERMISSION = '0000'


class AuthHandler:
    @staticmethod
    async def create_token_pair(payload, private_key, public_key):
        payload_copy = payload.copy()

        access_expire = datetime.utcnow() + timedelta(days=2)
        payload_copy.update({'expired': str(access_expire)})
        access_token = await AuthHandler.__create_token(payload=payload_copy, key=public_key)

        refresh_expire = datetime.utcnow() + timedelta(days=7)
        payload_copy.update({'expired': str(refresh_expire)})
        refresh_token = await AuthHandler.__create_token(payload=payload_copy, key=private_key)

        await AuthHandler.__verify_token(access_token)

        return access_token, refresh_token

    @staticmethod
    async def __create_token(payload, key):
        # token = jwt.encode(payload=payload, key=key, algorithm='RS256')  # For high level design
        token = jwt.encode(payload=payload, key=key)  # For low level design
        return token

    @staticmethod
    async def __verify_token(access_token):
        try:
            # decode = jwt.decode(access_token, key=public_key, algorithms=['RS256'])  # For high level design
            decoder = jwt.decode(access_token, options={'verify_signature': False})  # For low level design
        except Exception:
            raise AuthHandlerCreateTokenPairException

        return decoder

    @staticmethod
    async def check_authentication(request: Request):
        shop_id = request.headers.get(Header.CLIENT_ID.value)
        if not shop_id:
            raise BadRequestException(detail=ReasonStatusCode.CLIENT_ID_ERROR.value)

        access_token = request.headers.get(Header.AUTHORIZATION.value)
        if not access_token:
            raise BadRequestException(detail=ReasonStatusCode.AUTHENTICATION_ERROR.value)

        key_tokens_obj = await KeyTokenService.find_by_shop_id(shop_id=shop_id)
        if not key_tokens_obj:
            raise NotFoundException(detail=ReasonStatusCode.KEY_TOKEN_ERROR.value)

        decoder = await AuthHandler.__verify_token(access_token)
        if str(decoder['id']) != shop_id:
            raise UnauthorizedException(detail=ReasonStatusCode.AUTHENTICATION_ERROR.value)

        request.state.key_token_id = key_tokens_obj['_id']
