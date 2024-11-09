class ResponseDataHandler:
    @staticmethod
    async def response_data(obj: dict, fields: tuple):
        data = {}

        for field in fields:
            data.update({field: obj[field] if field != '_id' else str(obj[field])})

        return data
