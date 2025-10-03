from aiogram import Bot, Dispatcher
import os
from fastapi import FastAPI


bot = Bot(token=os.getenv("TOKEN"), parse_mode="HTML")
dp = Dispatcher()

ADMINS = ["B_lackSheep", "istanoki"]
admin_drafts = {
    ADMINS[0]: {},
    ADMINS[1]: {}
}

app = FastAPI()
