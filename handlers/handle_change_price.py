from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from filters.is_admin import is_admin
from models.db_models import async_session
from requests.product.update.change_price import change_price
from requests.product.get_variant import get_variant


router = Router()


class ChangePrice(StatesGroup):
    waiting_for_variant_id = State()
    waiting_for_new_price = State()
    waiting_for_confirmation = State()


@router.message(Command("changePrice"))
async def handle_change_price(message: types.Message, state: FSMContext):
    if not is_admin(message):
        await message.answer("У вас нет прав для этой команды.")
        await state.clear()
        return

    await message.answer("Введите ID варианта товара, цену которого хотите изменить:")
    await state.set_state(ChangePrice.waiting_for_variant_id)


@router.message(ChangePrice.waiting_for_variant_id)
async def process_variant_id(message: types.Message, state: FSMContext):
    async with async_session() as session:
        try:
            variant_id = int(message.text)
        except ValueError:
            await message.answer("Некорректный числовой ID. Примените команду заново")
            await state.clear()
            return

        variant = await get_variant(variant_id, session)
        if not variant:
            await message.answer("Вариант не найден. Примените команду заново.")
            await state.clear()
            return

        await state.update_data(variant=variant)

        await message.answer(f"Введите новую цену для варианта {variant_id}:")
        await state.set_state(ChangePrice.waiting_for_new_price)


@router.message(ChangePrice.waiting_for_new_price)
async def process_new_price(message: types.Message, state: FSMContext):
    try:
        new_price = float(message.text)
    except ValueError:
        await message.answer("Некорректная цена. Примените команду заново.")
        await state.clear()
        return

    await state.update_data(new_price=new_price)
    data = await state.get_data()
    variant = data["variant"]

    text = (
        "Вы уверены, что хотите изменить цену продукта?\n"
        f"ID: {variant.id}\n"
        f"Название: {variant.name}\n"
        f"Объем/масса: {variant.volume}\n"
        f"Цена: {variant.price} -> {new_price} BYN\n"
        f"Напишите 'Да' для подтверждения или 'Нет' для отмены"
    )

    await message.answer(text)
    await state.set_state(ChangePrice.waiting_for_confirmation)


@router.message(ChangePrice.waiting_for_confirmation)
async def process_confirmation(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        variant, new_price = data["variant"], data["new_price"]

        result = await change_price(variant.id, new_price)
        await message.answer(f"{result['status']}: {result['message']}")
    else:
        await message.answer("Операция отменена")

    await state.clear()
