import json
from datetime import datetime

from bson import ObjectId

from exceptions.misc import ResponseDataHandlerException


class ResponseDataHandler:
    @staticmethod
    async def response_data(obj_dict: dict, fields: tuple = None, exclude: tuple = None):
        data = {}

        json_data = json.loads(json.dumps(obj_dict, cls=DateTimeEncoder))

        if fields and exclude:
            raise ResponseDataHandlerException

        if not (fields or exclude):
            return json_data
        elif exclude:
            for d in json_data:
                if d not in exclude:
                    data.update({d: json_data[d]})
        else:
            for field in fields:
                data.update({field: json_data[field]})

        return data


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)

        return super(DateTimeEncoder, self).default(obj)
