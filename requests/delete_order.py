from models import async_session
from models import Order


async def delete_user(order_id):
    async with async_session() as session:
        async with session.begin():
            order = await session.get(Order, order_id)

            if not order:
                return {"status": "error", "message": "Order not found"}

            await session.delete(order)

        return {"status": "success", "message": "Order deleted"}
