from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from filters.is_admin import is_admin
from models import async_session
from requests.order.delete_order import delete_order
from requests.order.get_order import get_order


router = Router()


class DeleteOrder(StatesGroup):
    waiting_for_order_id = State()
    waiting_for_confirmation = State()


@router.message(Command("deleteOrder"))
async def start_delete_order(message: types.Message, state: FSMContext):
    if not is_admin(message):
        await message.answer("У вас нет прав для этой команды.")
        await state.clear()
        return

    await message.answer("Введите ID заказа, который хотите отменить:")
    await state.set_state(DeleteOrder.waiting_for_order_id)


@router.message(DeleteOrder.waiting_for_order_id)
async def process_delete_order(message: types.Message, state: FSMContext):
    async with async_session() as session:
        try:
            order_id = int(message.text)
        except ValueError:
            await message.answer("Некорректный числовой ID. Примените команду заново.")
            await state.clear()
            return

        order = await get_order(order_id, session)
        if not order:
            await message.answer("Такого заказа не существует.")
            await state.clear()
            return

        await state.update_data(order_id=order_id)

        text = (
            "Вы уверены, что хотите удалить заказ?\n\n"
            f"Order ID: {order.id}\n"
            f"Total cost: {order.total_cost} BYN\n"
            f"Order created at: {order.created_at}\n\n"
        )
        if order.notes:
            text += f"Notes: {order.notes}\n\n"

        for item in order.items:
            text += (
                f"Product name: {item.product_name}\n"
                f"Volume: {item.volume}\n"
                f"Price: {item.price} BYN\n"
                f"Quantity: {item.quantity}\n\n"
            )

        text += "Введите 'Да' для подтверждения или 'Нет' для отмены."

        await message.answer(text)
        await state.set_state(DeleteOrder.waiting_for_confirmation)


@router.message(DeleteOrder.waiting_for_confirmation)
async def confirm_delete_order(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        order_id = data.get("order_id")

        result = await delete_order(order_id)
        await message.answer(f"{result['message']}")
    else:
        await message.answer("Удаление отменено.")

    await state.clear()
