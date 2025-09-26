from models import async_session
from requests.get_orders import get_orders


async def delete_orders(tg_id):
    async with async_session() as session:
        async with session.begin():
            orders = await get_orders(tg_id, session)

            if not orders:
                return {"status": "error", "message": "Orders not found"}

            for order in orders:
                await session.delete(order)

        return {"status": "success", "message": f"Deleted {len(orders)} orders"}
