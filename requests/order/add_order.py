from models.db_models import Order, OrderItem
from datetime import datetime
import pytz


async def add_order(order_data, order_components, user_data, session):
    async with session.begin():
        order = Order(
            user_id=user_data.id,
            total_cost=order_data.total_cost,
            created_at=datetime.now(pytz.timezone("Europe/Minsk")),
            notes=order_data.notes,
            username=user_data.username,
            user_room=user_data.room,
            user_first_name=user_data.first_name
        )
        session.add(order)

        for component in order_components:
            order_item = OrderItem(
                order_id=component.order_id,
                category_name=component.category_name,
                product_name=component.product_name,
                volume=component.volume,
                price=component.price,
                quantity=component.quantity
            )
            session.add(order_item)

    return {"status": "success", "order_id": "Order placed"}
