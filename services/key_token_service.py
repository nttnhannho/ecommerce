from datetime import datetime

from pymongo import ReturnDocument

from dbs.mongodb import mongodb
from exceptions.exception import KeyTokenServiceCreateKeyTokenException
from models.key_token_model import KeyToken


class KeyTokenService:
    @staticmethod
    async def create_key_token(shop_id, private_key, public_key, refresh_token):
        try:
            # For low level design
            # key_token_obj = KeyToken(shop_id=shop_id, private_key=private_key, public_key=public_key, refresh_token=refresh_token)

            # For high level design
            collection = mongodb[KeyToken.__collection_name__]
            filter_ = {'shop_id': shop_id}
            update_fields = {
                '$set': {
                    'private_key': private_key,
                    'public_key': public_key,
                    'refresh_token': refresh_token,
                    'refresh_token_used': [],
                    'updated_at': datetime.utcnow(),
                }
            }
            key_token_obj = collection.find_one_and_update(filter_, update_fields, upsert=False, return_document=ReturnDocument.AFTER)
            if not key_token_obj:
                key_token_obj = KeyToken(shop_id=shop_id, private_key=private_key, public_key=public_key, refresh_token=refresh_token)
                key_token_dict = key_token_obj.model_dump()
                collection.insert_one(key_token_dict)
        except Exception:
            raise KeyTokenServiceCreateKeyTokenException

        return key_token_obj
