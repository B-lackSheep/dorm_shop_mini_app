from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from filters.is_admin import is_admin
from models import async_session
from requests.delete_product import delete_product
from requests.get_variant import get_variant


router = Router()


class DeleteOrder(StatesGroup):
    waiting_for_tg_id = State()
    result_ = State()


@router.message(Command("deleteOrder"))
async def start_delete_order(message: types.Message, state: FSMContext):
    if not is_admin(message):
        await message.answer("У вас нет прав для этой команды.")
        return

    await message.answer("Введите ID варианта товара, который хотите удалить:")
    await state.set_state(DeleteOrder.waiting_for_tg_id)


@router.message(DeleteOrder.waiting_for_tg_id)
async def process_tg_id(message: types.Message, state: FSMContext):
    try:
        tg_id = int(message.text)
    except ValueError:
        await message.answer("Введите корректный числовой ID.")
        return


