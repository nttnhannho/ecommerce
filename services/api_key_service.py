from dbs.mongodb import mongodb
from models.api_key import ApiKey


class ApiKeyService:
    @staticmethod
    def find_by_key(key):
        collection = mongodb[ApiKey.__collection_name__]
        key_obj = collection.find_one({'key': key})

        return key_obj
