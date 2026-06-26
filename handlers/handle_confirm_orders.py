from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from filters.is_admin import is_admin
from models.db_models import async_session
from requests.order.confirm_order import confirm_order
from requests.order.delete_order import delete_order
from requests.order.get_orders import get_orders


router = Router()


class ConfirmUserOrders(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_confirmation = State()


@router.message(Command("confirmUserOrders"))
async def start_confirm_order(message: types.Message, state: FSMContext):
    if not is_admin(message):
        await message.answer("У вас нет прав для этой команды.")
        await state.clear()
        return

    await message.answer("Введите ID заказа, оплату которого хотите подтвердить:")
    await state.set_state(ConfirmUserOrders.waiting_for_user_id)


@router.message(ConfirmUserOrders.waiting_for_user_id)
async def process_confirm_order(message: types.Message, state: FSMContext):
    async with async_session() as session:
        try:
            user_id = int(message.text)
        except ValueError:
            await message.answer("Некорректный числовой ID. Примените команду заново")
            await state.clear()
            return

        orders = await get_orders(user_id, session)
        if not orders:
            await message.answer("Заказы данного пользователя не найдены. Примените команду заново")
            await state.clear()
            return

        await state.update_data(orders=orders)

        text = "Вы уверены, что хотите подтвердить оплату заказа?\n\n"
        total_order_cost = 0
        for order in orders:
            text += (
                f"Order ID: {order.id}\n"
                f"Order cost: {order.total_cost} BYN\n"
                f"Order created at: {order.created_at}\n\n"
            )
            total_order_cost += order.total_cost

            for item in order.items:
                text += (
                    f"Product name: {item.product_name}\n"
                    f"Volume: {item.volume}\n"
                    f"Price: {item.price} BYN\n"
                    f"Quantity: {item.quantity}\n\n"
                )

        text += "Введите 'Да' для подтверждения или 'Нет' для отмены."

        await message.answer(text)
        await state.set_state(ConfirmUserOrders.waiting_for_confirmation)


@router.message(ConfirmUserOrders.waiting_for_confirmation)
async def confirm_user_orders(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        orders = data.get("orders")

        for order in orders:
            order_id = order.id

            sending_result = await confirm_order(order_id)
            deletion_result = await delete_order(order_id)

            if not sending_result['status'] == "success" or not deletion_result['status'] == "success":
                await state.clear()
                return await message.answer(
                    "Подтверждение заказов не удалось: "
                    f"{sending_result['message']}, "
                    f"{deletion_result['message']}"
                )
        await message.answer("Заказы подтверждены")
    else:
        await message.answer("Операция отменена")

    await state.clear()
