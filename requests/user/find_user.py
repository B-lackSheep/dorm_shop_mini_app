from models.db_models import User
from sqlalchemy import select


async def find_user(tg_id, session):
    result = await session.execute(
        select(User)
        .where(User.tg_id == tg_id)
    )

    return result.scalar_one_or_none()
