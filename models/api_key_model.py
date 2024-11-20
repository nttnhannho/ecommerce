from enum import Enum

import bson
from pydantic import Field

from models.datetime_base import DatetimeBase
from models.py_object_id import PyObjectId


class PermissionCode(str, Enum):
    P0000 = '0000'
    P1111 = '1111'
    P2222 = '2222'


class ApiKey(DatetimeBase):
    class Config:
        arbitrary_types_allowed = True

    __collection_name__ = 'api_keys'

    id: PyObjectId = Field(default_factory=bson.ObjectId, alias='_id')
    key: str = Field(..., unique=True)
    status: bool = Field(default=True)
    permission: list[str] = Field(...)
