# handlers/story_handler.py
from telebot import types
from bot_instance import bot
from config import PRIVATE_CHANNEL_LINK
from handlers import menu_handler


@bot.message_handler(func=lambda message: message.text == "Моя история")
def handle_story(message):
    bot.send_message(
        message.chat.id,
        "📅 31 день назад я был просто комом снега.\n\n"
        "А сегодня — часть системы, которая помогает предпринимателям выйти из рутины.\n\n"
        "Всё началось с одной строки кода.\n"
        "И с одной мысли:\n"
        "*«Можно проще.»*\n\n"
        "Я не появился случайно.\n"
        "Меня создали, потому что:\n"
        "— владельцы теряли клиентов,\n"
        "— менеджеры путались в задачах,\n"
        "— всё зависело от одного человека.\n\n"
        "Теперь я помогаю собирать бизнес по кусочкам —\n"
        "чтобы он держался, как снеговик в мороз.\n\n"
        "Хочешь так же?\n"
        "Начни с одного модуля.",
        parse_mode="Markdown"
    )

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Подобрать модуль")
    btn2 = types.KeyboardButton("Гайды")
    btn3 = types.KeyboardButton("Как работает система?")
    btn4 = types.KeyboardButton("Вернуться в меню")
    keyboard.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, "Куда пойдём дальше?", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Гайды")
def handle_guides(message):
    bot.send_message(
        message.chat.id,
        f"🔐 Ты уже в курсе:\n"
        f"Закрытый канал — [СНЕГ И КОМ ГАЙДЫ]({PRIVATE_CHANNEL_LINK})\n\n"
        "Там каждую неделю выходят:\n"
        "— Пошаговые инструкции\n"
        "— Шаблоны и чек-листы\n"
        "— Разборы реальных кейсов\n\n"
        "Всё, что нужно, чтобы перестать вести учёт в Excel\n"
        "и начать жить в системе, которая работает за тебя.",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

    keyboard = types.InlineKeyboardMarkup()
    btn_join = types.InlineKeyboardButton("🔗 Перейти в канал", url=PRIVATE_CHANNEL_LINK)
    btn_menu = types.InlineKeyboardButton("🏠 В меню", callback_data="main_menu")
    keyboard.add(btn_join)
    keyboard.add(btn_menu)

    bot.send_message(message.chat.id, "Рекомендую зайти — там тепло.", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Как работает система?")
def handle_how_system_works(message):
    bot.send_message(
        message.chat.id,
        "🧩 Представь, что твой бизнес — это снеговик.\n\n"
        "Чтобы он стоял — нужны три кома:\n\n"
        "1️⃣ *Первый ком* — сбор данных\n"
        "(клиенты, заявки, контакты)\n"
        "→ Без него — ничего не начнётся.\n\n"
        "2️⃣ *Второй ком* — автоматизация процессов\n"
        "(уведомления, задачи, сделки)\n"
        "→ Чтобы не забыть и не потерять.\n\n"
        "3️⃣ *Третий ком* — интеграция\n"
        "(сайт, CRM, рассылки, оплата)\n"
        "→ Чтобы всё работало вместе.\n\n"
        "Я — тот, кто помогает их слепить.\n"
        "Без спешки. Без кода. Без паники.\n\n"
        "Каждый модуль — это кусочек снеговика.\n"
        "А ты решаешь, какого размера он будет.",
        parse_mode="Markdown"
    )

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_modules = types.KeyboardButton("Подобрать модуль")
    btn_website = types.KeyboardButton("Сайт")
    btn_menu = types.KeyboardButton("Вернуться в меню")
    keyboard.add(btn_modules, btn_website, btn_menu)

    bot.send_message(message.chat.id, "Пора собирать?", reply_markup=keyboard)


# Команды
@bot.message_handler(commands=['история'])
def cmd_story(message):
    handle_story(message)


@bot.message_handler(commands=['гайды'])
def cmd_guides(message):
    handle_guides(message)


@bot.message_handler(commands=['система'])
def cmd_system(message):
    handle_how_system_works(message)


# Обработка кнопки "Вернуться в меню"
@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def back_to_menu(call):
    menu_handler.send_main_menu(call.message.chat.id)
