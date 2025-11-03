from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from filters.is_admin import is_admin
from models import async_session
from requests.product.delete_product import delete_product
from requests.product.get_variant import get_variant


router = Router()


class DeleteProduct(StatesGroup):
    waiting_for_variant_id = State()
    waiting_for_confirmation = State()


@router.message(Command("deleteProduct"))
async def start_delete_product(message: types.Message, state: FSMContext):
    if not is_admin(message):
        await message.answer("У вас нет прав для этой команды.")
        await state.clear()
        return

    await message.answer("Введите ID варианта товара, который хотите удалить:")
    await state.set_state(DeleteProduct.waiting_for_variant_id)


@router.message(DeleteProduct.waiting_for_variant_id)
async def process_delete_product(message: types.Message, state: FSMContext):
    async with async_session() as session:
        try:
            variant_id = int(message.text)
        except ValueError:
            await message.answer("Введите корректный числовой ID.")
            await state.clear()
            return

        variant = await get_variant(variant_id, session)
        if not variant:
            await message.answer("Вариант не найден. Введите команду заново.")
            await state.clear()
            return

        await state.update_data(variant_id=variant_id)

        text = (
            f"Вы уверены, что хотите удалить этот вариант?\n\n"
            f"ID: {variant.id}\n"
            f"Товар: {variant.product.product_name}\n"
            f"Объём: {variant.volume}\n"
            f"Цена: {variant.price} BYN\n"
            f"Количество: {variant.quantity}\n\n"
            "Напишите 'Да' для подтверждения или 'Нет' для отмены."
        )
        await message.answer(text)
        await state.set_state(DeleteProduct.waiting_for_confirmation)


@router.message(DeleteProduct.waiting_for_confirmation)
async def confirm_delete_product(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        variant_id = data.get("variant_id")

        result = await delete_product(variant_id)
        await message.answer(f"{result['message']}")
    else:
        await message.answer("Удаление отменено.")

    await state.clear()
