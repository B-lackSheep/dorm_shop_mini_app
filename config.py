from aiogram import Bot, Dispatcher
import os
from fastapi import FastAPI


bot = Bot(token=os.getenv("TOKEN"), parse_mode="HTML")
dp = Dispatcher()

ADMINS = os.getenv("ADMINS").split(",")

DEFAULT_VALUES = {
    "username": "Не установлен username",
    "first_name": "Нет данных об имени пользователя",
    "room": "Нет данных о комнате",
    "total_cost": 0.0,
    "product_name": "Имя товара не задано",
    "category_name": "Имя категории не задано",
    "volume": "Нет данных о массе/объеме",
    "price": 0.0,
    "quantity": 0
}

app = FastAPI()
