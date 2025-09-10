# bot_instance.py
from telebot import TeleBot
from config import TOKEN

# Создаём один экземпляр бота, который будет использоваться во всех хэндлерах
bot = TeleBot(TOKEN)
