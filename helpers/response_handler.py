class ResponseHandler:
    @staticmethod
    async def response_data(obj: dict, fields: tuple):
        data = {}

        for field in fields:
            data.update({field: obj[field]})

        return data
