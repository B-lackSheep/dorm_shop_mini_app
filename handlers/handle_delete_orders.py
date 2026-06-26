from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from filters.is_admin import is_admin
from models.db_models import async_session
from requests.order.delete_orders import delete_orders
from requests.order.get_orders import get_orders


router = Router()


class DeleteUserOrders(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_confirmation = State()


@router.message(Command("deleteUserOrders"))
async def start_delete_orders(message: types.Message, state: FSMContext):
    if not is_admin(message):
        await message.answer("У вас нет прав для этой команды.")
        await state.clear()
        return

    await message.answer("Введите ID пользователя, чьи заказы хотите отменить:")
    await state.set_state(DeleteUserOrders.waiting_for_user_id)


@router.message(DeleteUserOrders.waiting_for_user_id)
async def process_delete_orders(message: types.Message, state: FSMContext):
    async with async_session() as session:
        try:
            user_id = int(message.text)
        except ValueError:
            await message.answer("Некорректный числовой ID. Примените команду заново")
            await state.clear()
            return

        orders = await get_orders(user_id, session)
        if not orders:
            await message.answer("У этого пользователя нет заказов. Примените команду заново")
            await state.clear()
            return

        await state.update_data(user_id=user_id)

        text = f"Найдено заказов: {len(orders)}\n\n"
        total_cost_all = 0

        for order in orders:
            text += (
                f"Order ID: {order.id}\n"
                f"Order cost: {order.total_cost}\n BYN"
                f"Created at: {order.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
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

            total_cost_all += order.total_cost

        text += "Введите 'Да' для подтверждения или 'Нет' для отмены."

        await message.answer(text)
        await state.set_state(DeleteUserOrders.waiting_for_confirmation)


@router.message(DeleteUserOrders.waiting_for_confirmation)
async def confirm_delete_orders(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        user_id = data.get("user_id")

        result = await delete_orders(user_id)
        await message.answer(f"{result['status']}: {result['message']}")
    else:
        await message.answer("Операция отменена")

    await state.clear()
