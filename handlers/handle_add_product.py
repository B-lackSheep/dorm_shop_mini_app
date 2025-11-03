from aiogram import Router, types
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from filters.is_admin import is_admin
from models.db_models import async_session
from requests.product.add_product import add_product


router = Router()


class AddProduct(StatesGroup):
    waiting_for_category = State()
    waiting_for_name = State()
    waiting_for_volume = State()
    waiting_for_price = State()
    waiting_for_quantity = State()


@router.message(commands=["addProduct"])
async def start_add_product(message: types.Message, state: FSMContext):
    if not is_admin(message):
        await message.answer("У вас нет прав для этой команды")
        return

    await message.answer("Введите название категории:")
    await state.set_state(AddProduct.waiting_for_category)


@router.message(AddProduct.waiting_for_category)
async def process_category(message: types.Message, state: FSMContext):
    await state.update_data(category_name=message.text)
    await message.answer("Введите название товара:")
    await state.set_state(AddProduct.waiting_for_name)


@router.message(AddProduct.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(product_name=message.text)
    await message.answer("Введите объем/массу (например, '0.5 л'):")
    await state.set_state(AddProduct.waiting_for_volume)


@router.message(AddProduct.waiting_for_volume)
async def process_volume(message: types.Message, state: FSMContext):
    await state.update_data(volume=message.text)
    await message.answer("Введите цену в byn (например, 3.5):")
    await state.set_state(AddProduct.waiting_for_price)


@router.message(AddProduct.waiting_for_price)
async def process_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        await message.answer("Введите число (например, 99.9)")
        return

    await state.update_data(price=price)
    await message.answer("Введите количество (например, 5):")
    await state.set_state(AddProduct.waiting_for_quantity)


@router.message(AddProduct.waiting_for_quantity)
async def process_quantity(message: types.Message, state: FSMContext):
    try:
        quantity = int(message.text)
    except ValueError:
        await message.answer("Введите целое число (например, 10)")
        return

    async with async_session as session:
        data = await state.get_data()
        await add_product(data, session)

        await message.answer(
            f"Товар успешно добавлен:\n\n"
            f"Категория: {data['category_name']}\n"
            f"Название: {data['product_name']}\n"
            f"Объём: {data['volume']}\n"
            f"Цена: {data['price']}\n"
            f"Количество: {quantity}"
        )

        await state.clear()
