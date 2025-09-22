from models import User
from models import async_session


async def find_user(user_id):
    async with async_session() as session:
        user = await session.get(User, user_id)

        if not user:
            return None

        return user
