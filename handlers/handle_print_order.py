from aiogram import html
from datetime import datetime


async def handle_print_order(order_data):
    order_id_link = html.link(f"#{order_data['order_id']}",
                              f"tg://copy?text={order_data['order_id']}")
    user_id_link = html.link(f"#{order_data['user_id']}",
                             f"tg://copy?text={order_data['user_id']}")

    text = (
        "Ваш заказ:\n"
        f"ID заказа: {order_id_link}\n"
        f"ID пользователя: {user_id_link}\n"
        f"Дата заказа: {order_data['created_at']}\n\n"
    )
    total_cost = 0

    text += "Состав заказа:\n"
    for item in order_data['items']:
        text += f"Название товара: {item['name']}\n"
        text += f"Количество: {item['quantity']}\n"
        text += f"Цена: {item['price']} * {item['quantity']} = {item['price'] * item['quantity']}\n\n"

        total_cost += item['price'] * item['quantity']

    text += f"Итого: {total_cost} BYN"
    return text
