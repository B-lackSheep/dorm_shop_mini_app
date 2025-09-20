import telebot
import os


bot = telebot.TeleBot(os.getenv("TOKEN"))

ADMINS = ["@B_lackSheep", "@istanoki"]
admin_drafts = {
    ADMINS[0]: {},
    ADMINS[1]: {}
}
