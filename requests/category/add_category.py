from models.db_models import Category
from requests.category.get_category import get_category


async def add_category(category_name, session):
    async with session.begin():
        category = await get_category(category_name, session)
        if category:
            return {"status": "error", "message": "Category already exists"}

        category = Category(
            category_name=category_name
        )
        session.add(category)

    return {"status": "success", "order_id": "Order placed"}
