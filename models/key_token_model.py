import bson
from pydantic import Field

from models.datetime_base import DatetimeBase
from models.py_object_id import PyObjectId


class KeyToken(DatetimeBase):
    class Config:
        arbitrary_types_allowed = True

    __collection_name__ = 'tokens'

    id: PyObjectId = Field(default_factory=bson.ObjectId, alias='_id')
    shop_id: PyObjectId = Field(...)
    public_key: str = Field(...)
    refresh_token: list[str] = Field(default=[])
