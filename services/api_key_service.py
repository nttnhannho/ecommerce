from dbs.mongodb import mongodb
from exceptions.api_keys.exception import (
    ApiKeyServiceCreateApiKeyException,
    ApiKeyServiceRemoveAllException,
    ApiKeyServiceUpdateOneException,
    ApiKeyServiceInsertOneException,
    ApiKeyServiceFindByKeyException,
    ApiKeyServiceCountDocumentException,
)
from models.api_key_model import ApiKey


class ApiKeyService:
    collection = mongodb[ApiKey.__collection_name__]

    @staticmethod
    async def create_api_key(key, permission):
        try:
            api_key = ApiKey(key=key, permission=permission)
        except Exception:
            raise ApiKeyServiceCreateApiKeyException

        return api_key

    @staticmethod
    async def count_documents():
        try:
            count = ApiKeyService.collection.count_documents({})
        except Exception:
            raise ApiKeyServiceCountDocumentException

        return count

    @staticmethod
    async def find_by_key(key):
        try:
            api_key_obj = ApiKeyService.collection.find_one({'key': key})
        except Exception:
            raise ApiKeyServiceFindByKeyException

        return api_key_obj

    @staticmethod
    async def insert_one(data):
        try:
            ApiKeyService.collection.insert_one(data)
        except Exception:
            raise ApiKeyServiceInsertOneException

    @staticmethod
    async def update_one(filter_, update_fields):
        try:
            ApiKeyService.collection.update_one(filter=filter_, update=update_fields)
        except Exception:
            raise ApiKeyServiceUpdateOneException

    @staticmethod
    async def remove_all():
        try:
            ApiKeyService.collection.delete_many({})
        except Exception:
            raise ApiKeyServiceRemoveAllException
