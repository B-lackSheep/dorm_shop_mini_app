from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import async_session, Order, User


async def get_orders(tg_id, session):
    stmt = (
        select(Order)
        .join(Order.user)
        .options(selectinload(Order.items))
        .where(User.tg_id == tg_id)
    )
    result = await session.scalars(stmt)
    orders = result.all()

    return orders if orders else None
