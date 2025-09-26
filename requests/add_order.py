from models import async_session, User, Order, OrderItem
from requests.find_user import find_user
from datetime import datetime
import pytz


async def add_order(user_data, items_data, total_cost, notes: str = None):
    async with async_session() as session:
        async with session.begin():
            user = await find_user(user_data["tg_id"], session)
            if not user:
                user = User(**user_data)
                session.add(user)
                await session.flush()

            order = Order(
                user_id=user.id,
                total_cost=total_cost,
                notes=notes,
                created_at= datetime.now(pytz.timezone("Europe/Minsk"))
            )
            session.add(order)
            await session.flush()

            for item in items_data:
                order_item = OrderItem(
                    order_id=order.id,
                    product_name=item["product_name"],
                    volume=item["volume"],
                    price=item["price"],
                    quantity=item["quantity"]
                )
                session.add(order_item)

        return {"status": "success", "order_id": order.id}
