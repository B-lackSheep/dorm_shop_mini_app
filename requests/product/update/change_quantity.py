from models.db_models import async_session
from requests.product.get_variant import get_variant


async def change_quantity(variant_id, new_quantity):
    async with async_session() as session:
        async with session.begin():
            variant = await get_variant(variant_id, session)

            if not variant:
                return {"status": "error", "message": "Product not found"}

            variant.quantity = new_quantity

        return {"status": "success", "message": f"Quantity updated for product {variant_id}: {new_quantity}"}
