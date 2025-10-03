from config import app
from requests.get_products_by_category import get_products_by_category


@app.get("/category/{category_id}/{tg_id}")
async def get_category(category_id, tg_id):
    try:
        products = await get_products_by_category(category_id)

        if not products:
            return {"status": "error", "message": "Products in category not found"}

        dict_products = [
            {
                "name": product.product_name,
                "volume": product.variants.volume,
                "price": product.variants.price,
                "quantity": product.variants.quantity
            }
            for product in products]

        return {"status": "success", "products": dict_products}
    except Exception as e:
        return {"status": "error", "message": str(e)}

