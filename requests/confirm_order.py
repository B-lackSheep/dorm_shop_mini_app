from models import async_session
from requests.get_order import get_order


async def confirm_order(order_id):
    async with async_session() as session:
        order = get_order(order_id, session)

        if not order:
            return {"status": "error", "message": "Order wasn't found"}


