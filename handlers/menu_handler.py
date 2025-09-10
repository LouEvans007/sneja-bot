# handlers/menu_handler.py
from telebot import types
from bot_instance import bot
from config import WEBSITE_URL

def send_main_menu(chat_id):
    """Отправляет главное меню."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Подобрать модуль")
    btn2 = types.KeyboardButton("Моя история")
    btn3 = types.KeyboardButton("Гайды")
    btn4 = types.KeyboardButton("Как работает система?")
    btn5 = types.KeyboardButton("Сайт")
    btn6 = types.KeyboardButton("Помощь")

    keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6)

    bot.send_message(
        chat_id,
        "🧭 Привет снова! Я — Снежа.\n\n"
        "Выбери, куда пойдём:",
        reply_markup=keyboard
    )


# Обработка кнопок меню
@bot.message_handler(func=lambda message: message.text == "Помощь")
def handle_help(message):
    bot.send_message(
        message.chat.id,
        "Я могу:\n"
        "▫️ Проверить подписку → /start\n"
        "▫️ Дать доступ к гайдам → /гайды\n"
        "▫️ Помочь подобрать модуль → /подобрать\n"
        "▫️ Рассказать историю → /история\n"
        "▫️ Объяснить систему → /система\n"
        "▫️ Отправить ссылку на сайт → /сайт\n\n"
        "Напиши: *“СНЕГ”*, если потерялся.",
        parse_mode="Markdown"
    )


@bot.message_handler(func=lambda message: message.text == "Сайт")
def handle_website(message):
    keyboard = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("Перейти на сайт", url=f"{WEBSITE_URL}?ref=sneja")
    keyboard.add(btn)

    bot.send_message(
        message.chat.id,
        f"🌐 Официальный сайт: [{WEBSITE_URL}]({WEBSITE_URL}?ref=sneja)\n\n"
        "Там вы найдёте:\n"
        "— Полностью бесплатную вечную версию\n"
        "— Модули для расширения функций\n"
        "— Инструкции, поддержку и сообщество\n\n"
        "P.S. Напишите в чат поддержки: *“Снежа сказал(а)”* —\n"
        "мы скажем пару тёплых слов и покажем, где спрятаны лучшие гайды 😉",
        parse_mode="Markdown",
        reply_markup=keyboard
    )


# Кнопка "Вернуться в меню"
@bot.message_handler(func=lambda message: message.text == "Вернуться в меню")
def handle_back_to_menu(message):
    send_main_menu(message.chat.id)
