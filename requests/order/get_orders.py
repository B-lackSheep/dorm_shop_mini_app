from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.db_models import Order


async def get_orders(tg_id, session):
    stmt = (
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.user_tg_id == tg_id)
    )
    result = await session.scalars(stmt)
    orders = result.all()

    return orders if orders else None
