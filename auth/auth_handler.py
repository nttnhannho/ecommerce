from datetime import datetime, timedelta

import jwt

from exceptions.exception import AuthHandlerCreateTokenPairException


class AuthHandler:
    @staticmethod
    async def create_token_pair(payload, public_key, private_key):
        payload_copy = payload.copy()

        access_expire = datetime.utcnow() + timedelta(days=2)
        payload_copy.update({'expired': str(access_expire)})
        access_token = await AuthHandler.__create_token(payload=payload_copy, private_key=private_key)

        refresh_expire = datetime.utcnow() + timedelta(days=7)
        payload_copy.update({'expired': str(refresh_expire)})
        refresh_token = await AuthHandler.__create_token(payload=payload_copy, private_key=private_key)

        try:
            decode = jwt.decode(access_token, key=public_key, algorithms=['RS256'])
            print(decode)
        except Exception:
            raise AuthHandlerCreateTokenPairException

        return access_token, refresh_token

    @staticmethod
    async def __create_token(payload, private_key):
        token = jwt.encode(payload=payload, key=private_key, algorithm='RS256')
        return token
