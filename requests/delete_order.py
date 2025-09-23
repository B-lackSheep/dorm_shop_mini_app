from sqlalchemy import delete
from models import async_session
from models import Order


async def delete_order(tg_id):
    async with async_session() as session:
        async with session.begin():
            stmt = delete(Order).where(Order.tg_id == tg_id)
            result = await session.execute(stmt)

            if result.rowcount == 0:
                return {"status": "error", "message": "Orders not found"}

        return {"status": "success", "message": f"Deleted {result.rowcount} orders"}
