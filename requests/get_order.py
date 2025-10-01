from models import Order
from sqlalchemy import select
from sqlalchemy.orm import selectinload

async def get_order(order_id, session):
    result = await session.execute(
        select(Order)
        .options(selectinload(Order.items), selectinload(Order.user))
        .where(Order.id == order_id)
    )
    return result.scalar_one_or_none()
