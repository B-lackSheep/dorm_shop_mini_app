from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.db_models import ProductVariant


async def get_variant(variant_id, session):
    result = await session.execute(
        select(ProductVariant)
        .options(selectinload(ProductVariant.product))
        .where(ProductVariant.id == variant_id)
    )

    return result.scalar_one_or_none()
