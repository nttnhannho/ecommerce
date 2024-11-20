from fastapi import APIRouter

from routers.products.product import product_router
from routers.shops.shop import shop_router

router = APIRouter(prefix='/v1/api')
router.include_router(shop_router)
router.include_router(product_router)
