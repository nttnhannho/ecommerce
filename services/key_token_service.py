from exceptions.exception import KeyTokenServiceCreateKeyTokenException
from models.key_token_model import KeyToken


class KeyTokenService:
    @staticmethod
    async def create_key_token(shop_id, public_key):
        try:
            key_token = KeyToken(shop_id=shop_id, public_key=public_key)
        except Exception:
            raise KeyTokenServiceCreateKeyTokenException

        return key_token
