from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from filters.is_admin import is_admin
from models import async_session
from requests.product.get_products import get_products


router = Router()


class FindProduct(StatesGroup):
    waiting_for_product_name = State()


@router.message(Command("findProduct"))
async def handle_find_product(message: types.Message, state: FSMContext):
    if not is_admin(message):
        await message.answer("У вас нет прав для этой команды.")
        await state.clear()
        return

    await message.answer("Введите название продукта:")
    await state.set_state(FindProduct.waiting_for_product_name)


@router.message(FindProduct.waiting_for_product_name)
async def handle_product_name(message: types.Message, state: FSMContext):
    async with async_session() as session:
        product_name = message.text

        product_variants = await get_products(product_name, session)
        if not product_variants:
            await message.answer("Продукт с таким именем не найден.")
            await state.clear()
            return

        for product in product_variants:
            text = (
                f"ID варианта продукта: {product.variants.id}\n"
                f"Категория: {product.category.category_name}\n"
                f"Название: {product.product_name}\n"
                f"Объем/масса: {product.variants.volume}\n"
                f"Цена: {product.variants.price}\n"
                f"Количество: {product.variants.quantity}\n"
            )
            await message.answer(text)

        await state.clear()
