from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from filters.is_admin import is_admin
from models import async_session
from requests.confirm_order import confirm_order
from requests.delete_order import delete_order
from requests.get_order import get_order


router = Router()


class ConfirmOrder(StatesGroup):
    waiting_for_order_id = State()
    waiting_for_confirmation = State()


@router.message(Command("confirmOrder"))
async def start_confirm_order(message: types.Message, state: FSMContext):
    if not is_admin(message):
        await message.answer("У вас нет прав для этой команды.")
        await state.clear()
        return

    await message.answer("Введите ID заказа, оплату которого хотите подтвердить:")
    await state.set_state(ConfirmOrder.waiting_for_order_id)


@router.message(ConfirmOrder.waiting_for_order_id)
async def process_confirm_order(message: types.Message, state: FSMContext):
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
            "Вы уверены, что хотите подтвердить оплату заказа?\n\n"
            f"Order ID: {order.id}\n"
            f"Total cost: {order.total_cost} BYN\n"
            f"Order created at: {order.created_at}\n\n"
        )

        for item in order.items:
            text += (
                f"Product name: {item.product_name}\n"
                f"Volume: {item.volume}\n"
                f"Price: {item.price} BYN\n"
                f"Quantity: {item.quantity}\n\n"
            )

        text += "Введите 'Да' для подтверждения или 'Нет' для отмены."

        await message.answer(text)
        await state.set_state(ConfirmOrder.waiting_for_confirmation)


@router.message(ConfirmOrder.waiting_for_confirmation)
async def confirm_confirm_order(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        order_id = data.get("order_id")

        sending_result = await confirm_order(order_id)
        deletion_result = await delete_order(order_id)
        await message.answer(f"{sending_result['message']}, {deletion_result['message']}")
    else:
        await message.answer("Подтверждение отменено.")

    await state.clear()
