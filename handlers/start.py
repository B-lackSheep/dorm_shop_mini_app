from config import bot
import requests as rq


@bot.message_handler(commands=['start'])
async def handle_start_command(message):
    username = message.from_user.username
    user_id = message.chat.id
    first_name = message.from_user.first_name


