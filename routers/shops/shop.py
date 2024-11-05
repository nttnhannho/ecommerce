from fastapi import APIRouter

from models.shop_model import Shop
from services.shop_service import ShopService

shop_router = APIRouter(prefix='/shops')


@shop_router.post('/signup')
async def sign_up(request: Shop):
    return await ShopService.sign_up(request)
