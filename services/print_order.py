from aiogram import html


async def print_order(order_data, order_components, user_data):
    order_id_link = html.link(f"#{order_data['order_id']}",
                              f"tg://copy?text={order_data['order_id']}")
    user_id_link = html.link(f"#{user_data['user_id']}",
                             f"tg://copy?text={order_data['user_id']}")

    text = (
        "Ваш заказ:\n"
        f"ID заказа: {order_id_link}\n"
        f"ID пользователя: {user_id_link}\n"
        f"Дата заказа: {order_data['created_at']}\n\n"
    )

    if order_data['notes']:
        text += f"Примечание к заказу: {order_data['notes']}\n\n"
    total_cost = 0

    text += "Состав заказа:\n"
    for component in order_components:
        text += f"Название товара: {component['name']}\n"
        text += f"Объем/масса: {component['volume']}\n"
        text += f"Количество: {component['quantity']}\n"
        text += f"Цена: {component['price']} * {component['quantity']} = {component['price'] * component['quantity']}\n\n"

        total_cost += component['price'] * component['quantity']

    text += f"Итого: {total_cost} BYN"
    return text
