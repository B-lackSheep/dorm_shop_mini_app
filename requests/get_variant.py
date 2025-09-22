from models import ProductVariant


async def get_variant(variant_id, session):
    variant = await session.get(ProductVariant, variant_id)

    if not variant:
        return None

    return variant
