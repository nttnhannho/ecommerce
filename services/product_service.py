from bson import ObjectId

from core.error_response import BadRequestException, ReasonStatusCode as ErrorReasonStatusCode
from core.success_response import ReasonStatusCode as SuccessReasonStatusCode, CreatedResponse
from dbs.mongodb import mongodb
from exceptions.products.exception import (
    ClothingProductCreateException,
    ElectronicProductCreateException,
    FurnitureProductCreateException,
    ProductServiceInsertOneException,
    ProductCreateException,
    ClothingProductServiceInsertOneException,
    ElectronicProductServiceInsertOneException,
    FurnitureProductServiceInsertOneException,
    ProductServiceRemoveAllException,
    ClothingProductServiceRemoveAllException,
    ElectronicProductServiceRemoveAllException,
    FurnitureProductServiceRemoveAllException,
)
from helpers.response_data_handler import ResponseDataHandler
from models.product_model import (
    Product,
    ClothingProduct,
    ElectronicProduct,
    FurnitureProduct,
)


class ProductFactoryService:
    product_type_register = {}

    @staticmethod
    def register_product_type(ptype, class_ref):
        ProductFactoryService.product_type_register[ptype] = class_ref

    @staticmethod
    async def create(request):
        decoded_shop = request.state.decoded_shop
        shop_id = decoded_shop['id']

        payload = await request.json()
        ptype = payload.get('ptype')

        product_class = ProductFactoryService.product_type_register.get(ptype)
        if not product_class:
            raise BadRequestException(detail=ErrorReasonStatusCode.PRODUCT_TYPE_ERROR.value)

        new_product_dict = await product_class(**payload, shop_id=ObjectId(shop_id)).create()

        content = {
            'message': 'Created new product',
            'reason_status_code': SuccessReasonStatusCode.CREATED.value,
            'metadata': await ResponseDataHandler.response_data(obj_dict=new_product_dict),
            'options': {'limit': 10},
        }

        return CreatedResponse(content=content)


class ProductService:
    collection = mongodb[Product.__collection_name__]

    def __init__(self, name, thumbnail, description, price, quantity, ptype, shop_id, attributes):
        self.name = name
        self.thumbnail = thumbnail
        self.description = description
        self.price = price
        self.quantity = quantity
        self.ptype = ptype
        self.shop_id = shop_id
        self.attributes = attributes

    async def create(self, product_id=None):
        new_product = Product(**self.__dict__, id=product_id)
        if not new_product:
            raise ProductCreateException

        new_product_dict = new_product.model_dump(by_alias=True)
        await ProductService.insert_one(new_product_dict)

        return new_product_dict

    @staticmethod
    async def insert_one(data):
        try:
            ProductService.collection.insert_one(data)
        except Exception:
            raise ProductServiceInsertOneException

    @staticmethod
    async def remove_all():
        try:
            ProductService.collection.delete_many({})
        except Exception:
            raise ProductServiceRemoveAllException


class ClothingProductService(ProductService):
    collection = mongodb[ClothingProduct.__collection_name__]

    async def create(self, *args):
        new_clothing = ClothingProduct(**self.attributes, shop_id=self.shop_id)
        if not new_clothing:
            raise ClothingProductCreateException

        new_clothing_dict = new_clothing.model_dump(by_alias=True)
        await ClothingProductService.insert_one(new_clothing_dict)

        new_product = await super().create(new_clothing.id)
        return new_product

    @staticmethod
    async def insert_one(data):
        try:
            ClothingProductService.collection.insert_one(data)
        except Exception:
            raise ClothingProductServiceInsertOneException

    @staticmethod
    async def remove_all():
        try:
            ClothingProductService.collection.delete_many({})
        except Exception:
            raise ClothingProductServiceRemoveAllException


class ElectronicProductService(ProductService):
    collection = mongodb[ElectronicProduct.__collection_name__]

    async def create(self, *args):
        new_electronic = ElectronicProduct(**self.attributes, shop_id=self.shop_id)
        print(new_electronic)
        if not new_electronic:
            raise ElectronicProductCreateException

        new_electronic_dict = new_electronic.model_dump(by_alias=True)
        await ElectronicProductService.insert_one(new_electronic_dict)

        new_product = await super().create(new_electronic.id)
        return new_product

    @staticmethod
    async def insert_one(data):
        try:
            ElectronicProductService.collection.insert_one(data)
        except Exception:
            raise ElectronicProductServiceInsertOneException

    @staticmethod
    async def remove_all():
        try:
            ElectronicProductService.collection.delete_many({})
        except Exception:
            raise ElectronicProductServiceRemoveAllException


class FurnitureProductService(ProductService):
    furniture_collection = mongodb[FurnitureProduct.__collection_name__]

    async def create(self, *args):
        new_furniture = FurnitureProduct(**self.attributes, shop_id=self.shop_id)
        if not new_furniture:
            raise FurnitureProductCreateException

        new_furniture_dict = new_furniture.model_dump(by_alias=True)
        await FurnitureProductService.insert_one(new_furniture_dict)

        new_product = await super().create(new_furniture.id)
        return new_product

    @staticmethod
    async def insert_one(data):
        try:
            FurnitureProductService.collection.insert_one(data)
        except Exception:
            raise FurnitureProductServiceInsertOneException

    @staticmethod
    async def remove_all():
        try:
            FurnitureProductService.collection.delete_many({})
        except Exception:
            raise FurnitureProductServiceRemoveAllException


ProductFactoryService.register_product_type('Clothing', ClothingProductService)
ProductFactoryService.register_product_type('Electronic', ElectronicProductService)
ProductFactoryService.register_product_type('Furniture', FurnitureProductService)
