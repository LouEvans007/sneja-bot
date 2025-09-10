# handlers/start_handler.py
from telebot import types
from bot_instance import bot
from utils.subscription import is_subscribed
from handlers import menu_handler

@bot.message_handler(commands=['start'])
def handle_start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Я подписан(а)")
    keyboard.add(btn)

    bot.send_message(
        message.chat.id,
        "⛄ Привет! Я — Снежа.\n\n"
        "Я живу в системе Снег и ком и помогаю тем, кто хочет строить бизнес, а не чинить его.\n\n"
        "Ты написал(а) «СНЕГ» — значит, уже чувствуешь: можно проще.\n\n"
        "Но чтобы я доверил(а) тебе доступ…\n"
        "🔸 Подпишись на основной канал: @snegikom\n"
        "🔸 А потом скажи: *“Готово”* — и я открою дверь.",
        parse_mode="Markdown",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: "готово" in message.text.lower() or "я подписан" in message.text.lower())
def handle_subscription_check(message):
    if is_subscribed(message.chat.id):
        bot.send_message(
            message.chat.id,
            "✅ Отлично! Вижу, ты в теме.\n\n"
            "Открываю доступ к моему закрытому архиву:\n"
            "🔐 [СНЕГ И КОМ ГАЙДЫ](https://t.me/+L5FHukMqjvhiZWUy)\n\n"
            "Там каждую неделю выходят:\n"
            "— Пошаговые инструкции\n"
            "— Шаблоны и чек-листы\n"
            "— Разборы реальных кейсов\n\n"
            "И самое главное — всё, что нужно, чтобы начать автоматизацию без рутины.\n\n"
            "Хочешь, помогу подобрать, с чего начать?",
            parse_mode="Markdown"
        )
        menu_handler.send_main_menu(message.chat.id)
    else:
        bot.send_message(
            message.chat.id,
            "❌ Пока не вижу тебя в канале @snegikom.\n\n"
            "Подпишись — и нажми снова: *Готово*",
            parse_mode="Markdown"
        )
