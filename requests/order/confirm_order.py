from models.db_models import async_session, Status
from requests.order.get_order import get_order


async def confirm_order(order_id):
    async with async_session() as session:
        async with session.begin():
            order = await get_order(order_id, session)

            if not order:
                return {"status": "error", "message": "Order wasn't found"}

            if order.status == Status.CONFIRMED:
                return {"status": "error", "message": "Order already confirmed"}

            order.status = Status.CONFIRMED

        return {"status":"success", "message":"The order has been confirmed and sent for analysis"}
