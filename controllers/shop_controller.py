from services.shop_service import ShopService


class ShopController:
    @staticmethod
    async def sign_up(request):
        return await ShopService.sign_up(request)

    @staticmethod
    async def log_in(request):
        return await ShopService.log_in(request)
