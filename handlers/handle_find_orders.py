from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from filters.is_admin import is_admin
from requests.order.get_orders import get_orders
from models.db_models import async_session


router = Router()


class FindOrders(StatesGroup):
    waiting_for_user_id = State()


@router.message(Command("findOrders"))
async def handle_find_orders(message: types.Message, state: FSMContext):
    if not is_admin(message):
        await message.answer("У вас нет прав для этой команды.")
        await state.clear()
        return

    await message.answer("Введите id пользователя:")
    await state.set_state(FindOrders.waiting_for_user_id)


@router.message(FindOrders.waiting_for_user_id)
async def process_user_id(message: types.Message, state: FSMContext):
    async with async_session() as session:
        try:
            user_id = int(message.text)
        except ValueError:
            await message.answer("Некорректный ID пользователя. Примените команду заново")
            await state.clear()
            return

        orders = await get_orders(user_id, session)
        if not orders:
            await message.answer("У этого пользователя нет заказов. Примените команду заново")
            await state.clear()
            return

        text = (
            f"Найдено заказов: {len(orders)}\n"
            f"Пользователя: {orders[0].user.first_name} {orders[0].user.username}\n"
            f"ID пользователя: {orders[0].user.tg_id}\n"
        )
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

        text += f"Total cost: {total_cost_all} BYN"
        await message.answer(text)
        await state.clear()
