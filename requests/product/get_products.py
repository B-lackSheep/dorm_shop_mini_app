from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.db_models import Product


async def get_products(product_name, session):
    result = await session.execute(
        select(Product)
        .options(
            selectinload(Product.variants),
            selectinload(Product.category)
        )
        .where(Product.product_name.ilike(f"%{product_name}%"))
    )
    products = result.scalars().all()

    return products
