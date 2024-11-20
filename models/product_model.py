from enum import Enum
from typing import Optional, Union

import bson
from pydantic import Field

from models.datetime_base import DatetimeBase
from models.py_object_id import PyObjectId


class ProductType(str, Enum):
    ELECTRONIC = 'Electronic'
    CLOTHING = 'Clothing'


class Product(DatetimeBase):
    __collection_name__ = 'products'

    id: PyObjectId = Field(default_factory=bson.ObjectId, alias='_id')
    name: str = Field(...)
    thumbnail: str = Field(...)
    description: Optional[str] = ''
    price: float = Field(...)
    quantity: int = Field(...)
    ptype: ProductType = Field(...)
    attributes: Union[int, float, str, dict] = Field(...)
    shop_id: PyObjectId = Field(...)


class ClothingProduct(DatetimeBase):
    __collection_name__ = 'clothes'

    id: PyObjectId = Field(default_factory=bson.ObjectId, alias='_id')
    brand: str = Field(...)
    size: Optional[str] = ''
    material: Optional[str] = ''
    shop_id: PyObjectId = Field(...)


class ElectronicProduct(DatetimeBase):
    __collection_name__ = 'electronics'

    id: PyObjectId = Field(default_factory=bson.ObjectId, alias='_id')
    manufacturer: str = Field(...)
    model: Optional[str] = ''
    color: Optional[str] = ''
    shop_id: PyObjectId = Field(...)


class FurnitureProduct(DatetimeBase):
    __collection_name__ = 'furnitures'

    id: PyObjectId = Field(default_factory=bson.ObjectId, alias='_id')
    brand: str = Field(...)
    size: Optional[str] = ''
    material: Optional[str] = ''
    shop_id: PyObjectId = Field(...)
