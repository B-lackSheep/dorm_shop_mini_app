from models import Order


async def get_order(order_id, session):
        order = await session.get(Order, order_id)

        if not order:
            return None

        return order
