from models.db_models import async_session
from requests.product.get_variant import get_variant


async def change_name(variant_id, new_name):
    async with async_session() as session:
        async with session.begin():
            variant = await get_variant(variant_id, session)

            if not variant:
                return {"status": "error", "message": "Product not found"}

            variant.product.product_name = new_name

        return {"status": "success", "message": f"Product name updated for product {variant_id}: {new_name}"}
