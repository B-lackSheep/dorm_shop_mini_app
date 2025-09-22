from aiogram import Router, types
from requests.add_user import add_user

router = Router()

@router.message(commands=["start"])
async def handle_start_command(message: types.Message):
    username = message.from_user.username
    tg_id = message.chat.id
    first_name = message.from_user.first_name

    result = await add_user(tg_id, username, first_name)
    print(result)

    mess = (
        "Приветствую тебя в <b>Общажной лавке</b>!\n\n"
        "Тебя ожидает самый большой ассортимент и удобнейший сервис.\n\n"
        "Скорее нажимай на кнопку <b>лавка</b>"
    )
    await message.answer(mess)
