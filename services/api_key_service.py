from dbs.mongodb import mongodb
from exceptions.exception import ApiKeyServiceCreateApiKeyException
from models.api_key import ApiKey


class ApiKeyService:
    @staticmethod
    async def create_api_key(key, permission):
        try:
            api_key = ApiKey(key=key, permission=permission)
        except Exception:
            raise ApiKeyServiceCreateApiKeyException

        return api_key

    @staticmethod
    async def find_by_key(key):
        collection = mongodb[ApiKey.__collection_name__]
        api_key_obj = collection.find_one({'key': key})

        return api_key_obj
