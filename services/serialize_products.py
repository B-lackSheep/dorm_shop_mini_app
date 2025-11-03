from requests.product.get_products_by_category import get_products_by_category


async def serialize_products(category_id):
    products = await get_products_by_category(category_id)
    if not products:
        return None

    serialized_products = [product.model_dump() for product in products]

    return serialized_products
