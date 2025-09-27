from models import async_session, SaleItem, Sale
from requests.find_user import find_user
from requests.get_order import get_order


async def order_to_sale(order_id, user_id):
    async with async_session() as session:
        async with session.begin():
            user = await find_user(user_id, session)
            if not user:
                return {"status": "error", "message": "User not found"}

            order = await get_order(order_id, session)
            if not order:
                return {"status": "error", "message": "Order not found"}

            sale = Sale(
                user_id=user_id,
                total_cost=order.total_cost,
                created_at=order.created_at,
                user_room=user.room,
                user_name=user.first_name
            )
            session.add(sale)
            session.flush()

            sale_item = SaleItem(
                sale_id=sale.id,
                product_name=order.product_name,
                volume=order.volume,
                price=order.price,
                quantity=order.quantity
            )

            session.add(sale_item)

        return {"status": "success", "message": "Order was send to analytics"}
