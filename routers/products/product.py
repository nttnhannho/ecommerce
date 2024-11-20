from fastapi import APIRouter, Depends
from starlette.requests import Request

from auth.auth_handler import AuthHandler
from controllers.product_controller import ProductController

product_router = APIRouter(prefix='/products', dependencies=[Depends(AuthHandler.check_authentication)])


@product_router.post('')
async def create(request: Request):
    return await ProductController.create(request)
