from models.db_models import async_session, User
from requests.user.find_user import find_user


async def add_user(tg_id, username, first_name):
    async with async_session() as session:
        async with session.begin():
            user = await find_user(tg_id, session)

            if user:
                return {"status": "error", "message": "The user has already been added"}

            user = User(
                tg_id=tg_id,
                username=username,
                first_name=first_name
            )
            session.add(user)

        return {"status": "success", "message": "User added"}
