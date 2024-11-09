import bson
from pydantic import Field

from models.datetime_base import DatetimeBase
from models.py_object_id import PyObjectId


class KeyToken(DatetimeBase):
    class Config:
        arbitrary_types_allowed = True

    __collection_name__ = 'key_tokens'

    id: PyObjectId = Field(default_factory=bson.ObjectId, alias='_id')
    shop_id: PyObjectId = Field(...)
    private_key: str = Field(...)
    public_key: str = Field(...)
    refresh_token: str = Field(...)
    refresh_token_used: list[str] = Field(default=[])
