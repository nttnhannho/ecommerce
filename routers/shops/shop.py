from fastapi import APIRouter, Depends
from starlette.requests import Request

from auth.auth_handler import AuthHandler
from controllers.shop_controller import ShopController

shop_router = APIRouter(prefix='/shops')


@shop_router.post('/signup')
async def sign_up(request: Request):
    return await ShopController.sign_up(request)


@shop_router.post('/login')
async def log_in(request: Request):
    return await ShopController.log_in(request)


@shop_router.post('/logout', dependencies=[Depends(AuthHandler.check_authentication)])
async def log_out(request: Request):
    return await ShopController.log_out(request)


@shop_router.post('/handle-token', dependencies=[Depends(AuthHandler.check_authentication_for_handling_token)])
async def handle_token(request: Request):
    return await ShopController.handle_token(request)
