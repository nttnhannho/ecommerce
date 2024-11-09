from datetime import datetime, timedelta

import jwt

from exceptions.exception import AuthHandlerCreateTokenPairException


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

        try:
            # decode = jwt.decode(access_token, key=public_key, algorithms=['RS256'])  # For high level design
            jwt.decode(access_token, options={'verify_signature': False})  # For low level design
        except Exception:
            raise AuthHandlerCreateTokenPairException

        return access_token, refresh_token

    @staticmethod
    async def __create_token(payload, key):
        # token = jwt.encode(payload=payload, key=key, algorithm='RS256')  # For high level design
        token = jwt.encode(payload=payload, key=key)  # For low level design
        return token
