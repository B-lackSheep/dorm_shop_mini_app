from sqlalchemy import select
from models import async_session
from models import Order


async def get_orders(tg_id):
    async with async_session() as session:
        stmt = select(Order).where(Order.tg_id == tg_id)
        orders = await session.scalars(stmt)

        if not orders:
            return None

        return orders
