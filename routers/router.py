from fastapi import APIRouter

from routers.shops.shop import shop_router

router = APIRouter(prefix='/v1/api')
router.include_router(shop_router)
