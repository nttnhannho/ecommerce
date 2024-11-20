from datetime import datetime

from bson import ObjectId
from pymongo import ReturnDocument

from dbs.mongodb import mongodb
from exceptions.key_tokens.exception import (
    KeyTokenServiceCreateKeyTokenException,
    KeyTokenServiceFindOneAndUpdateException,
    KeyTokenServiceInsertOneException,
    KeyTokenServiceFindByShopIdException,
    KeyTokenServiceRemoveByIdException,
    KeyTokenServiceFindByRefreshTokenUsedException,
    KeyTokenServiceRemoveByShopIdException,
    KeyTokenServiceFindByRefreshTokenException,
    KeyTokenServiceRemoveAllException,
    KeyTokenServiceUpdateOneException,
    KeyTokenServiceFindOneException,
)
from models.key_token_model import KeyToken


class KeyTokenService:
    collection = mongodb[KeyToken.__collection_name__]

    @staticmethod
    async def create_key_token(shop_id, private_key, public_key, refresh_token):
        try:
            # For low level design
            # key_token_obj = KeyToken(
            #     shop_id=shop_id,
            #     private_key=private_key,
            #     public_key=public_key,
            #     refresh_token=refresh_token,
            # )

            # For high level design
            filter_ = {'shop_id': shop_id}
            update = {
                '$set': {
                    'private_key': private_key,
                    'public_key': public_key,
                    'refresh_token': refresh_token,
                    'refresh_token_used': [],
                    'updated_at': datetime.utcnow(),
                }
            }
            key_token_obj = await KeyTokenService.find_one_and_update(
                filter_,
                update,
                upsert=False,
                return_document=ReturnDocument.AFTER,
            )
            if not key_token_obj:
                key_token_obj = KeyToken(
                    shop_id=shop_id,
                    private_key=private_key,
                    public_key=public_key,
                    refresh_token=refresh_token,
                )
                key_token_dict = key_token_obj.model_dump(by_alias=True)
                await KeyTokenService.insert_one(key_token_dict)
        except Exception:
            raise KeyTokenServiceCreateKeyTokenException

        return key_token_obj

    @staticmethod
    async def find_one_and_update(filter_, update, upsert, return_document):
        try:
            key_token_obj = KeyTokenService.collection.find_one_and_update(
                filter=filter_,
                update=update,
                upsert=upsert,
                return_document=return_document,
            )
        except Exception:
            raise KeyTokenServiceFindOneAndUpdateException

        return key_token_obj

    @staticmethod
    async def insert_one(key_token):
        try:
            KeyTokenService.collection.insert_one(key_token)
        except Exception:
            raise KeyTokenServiceInsertOneException

    @staticmethod
    async def find_by_shop_id(shop_id):
        try:
            key_token_obj = KeyTokenService.collection.find_one({'shop_id': ObjectId(shop_id)})
        except Exception:
            raise KeyTokenServiceFindByShopIdException

        return key_token_obj

    @staticmethod
    async def remove_by_id(key_token_id):
        try:
            result = KeyTokenService.collection.delete_one({'_id': ObjectId(key_token_id)})
        except Exception:
            raise KeyTokenServiceRemoveByIdException

        return result

    @staticmethod
    async def find_by_refresh_token_used(refresh_token):
        try:
            key_token_obj = KeyTokenService.collection.find_one({'refresh_token_used': refresh_token})
        except Exception:
            raise KeyTokenServiceFindByRefreshTokenUsedException

        return key_token_obj

    @staticmethod
    async def remove_by_shop_id(shop_id):
        try:
            result = KeyTokenService.collection.delete_one({'shop_id': shop_id})
        except Exception:
            raise KeyTokenServiceRemoveByShopIdException

        return result

    @staticmethod
    async def find_by_refresh_token(refresh_token):
        try:
            result = KeyTokenService.collection.find_one({'refresh_token': refresh_token})
        except Exception:
            raise KeyTokenServiceFindByRefreshTokenException

        return result

    @staticmethod
    async def remove_all():
        try:
            KeyTokenService.collection.delete_many({})
        except Exception:
            raise KeyTokenServiceRemoveAllException

    @staticmethod
    async def update_one(filter_, update):
        try:
            KeyTokenService.collection.update_one(filter_, update)
        except Exception:
            raise KeyTokenServiceUpdateOneException

    @staticmethod
    async def find_one(data):
        try:
            result = KeyTokenService.collection.find_one(data)
        except Exception:
            raise KeyTokenServiceFindOneException

        return result
