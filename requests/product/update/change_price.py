from models.db_models import async_session
from requests.product.get_variant import get_variant


async def change_price(variant_id, new_price):
    async with async_session() as session:
        async with session.begin():
            variant = await get_variant(variant_id, session)

            if not variant:
                return {"status": "error", "message": "Product not found"}

            variant.price = new_price

        return {"status": "success", "message": f"Price updated for product {variant_id}"}
