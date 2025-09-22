from aiogram import types
from config import ADMINS


def is_admin(message: types.Message) -> bool:
    username = message.from_user.username
    if not username:
        return False
    return f"@{username}" in ADMINS
