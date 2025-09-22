from sqlalchemy import select, func
from models import async_session, Product, ProductVariant
from requests.get_variant import get_variant


async def delete_product(variant_id):
    async with async_session() as session:
        async with session.begin():
            variant = await get_variant(variant_id, session)

            if not variant:
                return {"status": "error", "message": "Variant not found"}

            product_id = variant.product_id

            await session.delete(variant)
            await session.flush()

            stmt = select(func.count(ProductVariant.id)).where(ProductVariant.product_id == product_id)
            variants_amount = await session.scalar(stmt)

            if variants_amount == 0:
                product = await session.get(Product, product_id)
                if product:
                    await session.delete(product)

        return {"status": "success", "message": "Variant deleted"}
