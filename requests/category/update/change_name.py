from models.db_models import async_session
from requests.category.get_category import get_category


async def change_name(category_name, new_name):
    async with async_session() as session:
        async with session.begin():
            category = await get_category(category_name, session)

            if not category:
                return {"status": "error", "message": "Category not found"}

            category.category_name = new_name

        return {"status": "success", "message": f"Category name updated: {new_name}"}
