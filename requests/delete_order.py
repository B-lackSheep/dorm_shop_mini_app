from models import async_session
from requests.get_order import get_order


async def delete_order(order_id):
    async with async_session() as session:
        async with session.begin():
            order = await get_order(order_id, session)

            if not order:
                return {"status": "error", "message": "Order not found"}

            await session.delete(order)

        return {"status": "success", "message": f"Deleted order {order_id}"}
