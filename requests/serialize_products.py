from requests.get_products import get_products
from schemas import ProductSchema


async def serialize_product(category_id):
    products = await get_products(category_id)
    if not products:
        return None

    serialized_products = ProductSchema.model_validate(products).model_dump()

    return serialized_products
