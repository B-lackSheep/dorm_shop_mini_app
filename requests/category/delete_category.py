from models.db_models import async_session
from requests.category.get_category import get_category


async def delete_category(category_name):
    async with async_session() as session:
        async with session.begin():
            category = await get_category(category_name, session)
            if not category:
                return {"status": "error", "message": "Category not found"}

            await session.delete(category)

        return {"status": "success", "message": f"Deleted category for {category_name}"}
