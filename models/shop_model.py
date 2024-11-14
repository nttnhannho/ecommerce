from enum import Enum

import bson
from pydantic import EmailStr, Field, field_validator

from helpers.field_validator import strip
from models.datetime_base import DatetimeBase
from models.py_object_id import PyObjectId


class ShopStatus(str, Enum):
    INACTIVE = 'inactive'
    ACTIVE = 'active'


class ShopRole(str, Enum):
    SHOP = 'SHOP'
    WRITER = 'WRITER'
    EDITOR = 'EDITOR'
    ADMIN = 'ADMIN'


class Shop(DatetimeBase):
    class Config:
        arbitrary_types_allowed = True

    __collection_name__ = 'shops'

    id: PyObjectId = Field(default_factory=bson.ObjectId, alias='_id')
    name: str = Field(..., max_length=150)
    email: EmailStr = Field(...)
    password: str = Field(...)
    status: ShopStatus = Field(default=ShopStatus.INACTIVE)
    verified: bool = Field(default=False)
    roles: list[str] = Field(default=[])

    @field_validator('name')
    def strip_name(cls, name):
        return strip(name)

    @field_validator('email')
    def strip_email(cls, email):
        return strip(email)
