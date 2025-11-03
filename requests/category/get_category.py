from models.db_models import Category
from sqlalchemy import select


async def get_category(category_name, session):
    async with session.begin():
        result = await session.execute(
            select(Category)
            .where(Category.category_name == category_name)
        )
        return result.scalar_one_or_none()
