from fastapi import APIRouter

from controllers.shop_controller import ShopController
from models.shop_model import Shop, ShopLogin

shop_router = APIRouter(prefix='/shops')


@shop_router.post('/signup')
async def sign_up(request: Shop):
    return await ShopController.sign_up(request)


@shop_router.post('/login')
async def log_in(request: ShopLogin):
    return await ShopController.log_in(request)
