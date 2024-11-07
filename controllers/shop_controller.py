from services.shop_service import ShopService


class ShopController:
    @staticmethod
    async def sign_up(request):
        return await ShopService.sign_up(request)
