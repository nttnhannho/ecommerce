from services.product_service import ProductFactoryService


class ProductController:
    @staticmethod
    async def create(request):
        return await ProductFactoryService.create(request)
