from models import async_session, Sale, SaleItem
from requests.get_order import get_order


async def confirm_order(order_id):
    async with async_session() as session:
        async with session.begin():
            order = await get_order(order_id, session)

            if not order:
                return {"status": "error", "message": "Order wasn't found"}

            sale = Sale(
                user_id=order.user_id,
                total_cost=order.total_cost,
                created_at=order.created_at,
                user_room=order.user.room,
                user_name=order.user.first_name
            )

            session.add(sale)
            await session.flush()

            for order_item in order.items:
                sale_item = SaleItem(
                    sale_id=sale.id,
                    product_name=order_item.product_name,
                    volume=order_item.volume,
                    price=order_item.price,
                    quantity=order_item.quantity
                )

                session.add(sale_item)

            return {"status":"success", "message":"Order sent to analytics"}

