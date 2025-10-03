from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import ProductVariant


async def get_variant(variant_id, session):
    result = await session.execute(
        select(ProductVariant)
        .options(selectinload(ProductVariant.product))
        .where(ProductVariant.id == variant_id)
    )
    variant = result.scalar_one_or_none()

    return variant
