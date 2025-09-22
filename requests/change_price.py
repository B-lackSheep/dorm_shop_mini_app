from models import async_session
from requests.get_variant import get_variant


async def change_price(variant_id, new_price):
    async with async_session() as session:
        async with session.begin():
            variant = await get_variant(variant_id, session)

            if not variant:
                return {"status": "error", "message": "Variant not found"}

            variant.price = new_price

        return {"status": "success", "message": f"Price updated for variant {variant_id}"}
