from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import async_session, Product


async def get_products_by_category(category_id):
    async with async_session() as session:
        products = await session.scalars(
            select(Product)
            .where(Product.category_id == category_id)
            .options(
                selectinload(Product.variants),
                selectinload(Product.category)
            )
        )
        if not products:
            return None

        return products
