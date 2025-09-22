from models import async_session
from requests.get_variant import get_variant


async def change_quantity(variant_id, new_quantity):
    async with async_session() as session:
        async with session.begin():
            variant = await get_variant(variant_id, session)

            if not variant:
                return {"status": "error", "message": "Variant not found"}

            variant.quantity = new_quantity

        return {"status": "success", "message": f"Quantity updated for quantity {variant_id}"}
