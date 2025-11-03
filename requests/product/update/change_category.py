from models.db_models import async_session
from requests.product.get_variant import get_variant


async def change_category(variant_id, new_category_id):
    async with async_session() as session:
        async with session.begin():
            variant = await get_variant(variant_id, session)

            if not variant:
                return {"status": "error", "message": "Product not found"}

            variant.product.category_id = new_category_id

        return {"status": "success", "message": f"Category updated for product {variant_id}: {new_category_id}"}

