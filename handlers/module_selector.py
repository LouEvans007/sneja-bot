# handlers/module_selector.py
from telebot import types
from bot_instance import bot
from config import WEBSITE_URL
from handlers import menu_handler

# === База модулей ===
MODULES_DB = {
    "data_loss": {
        "name": "Очистка данных",
        "category": "Инструменты",
        "emoji": "🧹",
        "metaphor": "как совок для мусора",
        "description": "Находит дубликаты контактов и компаний, объединяет записи и чистит базу. Чистая CRM — меньше ошибок, больше доверия.",
        "url": f"{WEBSITE_URL}/marketplace/68a3a5104ce252ca0ea1ec06"
    },
    "manual_work": {
        "name": "Задачи",
        "category": "Управление задачами",
        "emoji": "📌",
        "metaphor": "как напоминалка, которая никогда не забудет",
        "description": "Ставьте задачи, назначайте исполнителей, отслеживайте статусы в kanban-доске. Работа станет прозрачной и контролируемой.",
        "url": f"{WEBSITE_URL}/marketplace/68a3a8f04ce252ca0ea1ec0f"
    },
    "client_disorder": {
        "name": "Продажи",
        "category": "Продажи и CRM",
        "emoji": "💼",
        "metaphor": "как менеджер, который помнит всё",
        "description": "Управляйте сделками от заявки до оплаты. Видите все этапы, формируйте КП, выставляйте счёт и отслеживайте аналитику.",
        "url": f"{WEBSITE_URL}/marketplace/68a23b9796a0224c964d1ff0"
    },
    "dev_dependence": {
        "name": "Веб-сайт",
        "category": "Веб-сайт",
        "emoji": "🌐",
        "metaphor": "как дом, который вы построили сами",
        "description": "Создайте сайт без программиста. Перетаскивайте блоки, добавляйте страницы, магазин или блог. Полный контроль — ваш сервер, ваши данные.",
        "url": f"{WEBSITE_URL}/marketplace/689f8b1104440059e647bd48"
    },
    "dont_know_start": {
        "name": "Маркетинговая карточка",
        "category": "Маркетинг",
        "emoji": "🎯",
        "metaphor": "как план, который оживает",
        "description": "Планируйте кампании в карточках, назначайте задачи, интегрируйте с email и CRM. Никакого хаоса — только порядок и результат.",
        "url": f"{WEBSITE_URL}/marketplace/68a3a0eb4ce252ca0ea1ebf3"
    }
}

# Глобальный флаг: кто сейчас в диалоге подбора
waiting_for_pain = set()

# === Обработчик: "Подобрать модуль" ===
@bot.message_handler(func=lambda message: message.text == "Подобрать модуль")
def ask_pain_point(message):
    global waiting_for_pain

    bot.send_message(
        message.chat.id,
        "⛄ Снежа спрашивает:\n\n"
        "Какая боль сейчас сильнее?\n\n"
        "1. Постоянно теряю данные\n"
        "2. Всё делается вручную\n"
        "3. Нет порядка в клиентах\n"
        "4. Зависим от разработчиков\n"
        "5. Не знаю, с чего начать\n\n"
        "Напиши цифру.",
    )
    waiting_for_pain.add(message.chat.id)


# === Универсальный хэндлер для цифры 1–5, только если пользователь в процессе ===
@bot.message_handler(func=lambda message: message.text.strip() in ["1", "2", "3", "4", "5"])
def handle_pain_input(message):
    global waiting_for_pain

    if message.chat.id not in waiting_for_pain:
        # Это не часть диалога подбора — игнорируем как обычный текст
        return

    # Убираем из ожидания
    waiting_for_pain.discard(message.chat.id)

    choice_map = {
        "1": "data_loss",
        "2": "manual_work",
        "3": "client_disorder",
        "4": "dev_dependence",
        "5": "dont_know_start"
    }

    chosen_key = choice_map[message.text.strip()]

    recommend_module(message.chat.id, chosen_key)


def recommend_module(chat_id, choice_key):
    module = MODULES_DB.get(choice_key)
    if not module:
        bot.send_message(chat_id, "Не удалось определить подходящий модуль. Попробуй ещё раз.")
        return

    text = (
        f"{module['emoji']} Понял(а)! Тебе нужен модуль: *{module['name']}*\n\n"
        f"Он как {module['metaphor']}:\n"
        f"▫️ {module['description']}\n\n"
        f"🎯 Подходит для тех, кто хочет навести порядок в *{module['category']}*."
    )

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn_more = types.InlineKeyboardButton("Подробнее", callback_data=f"more_{choice_key}")
    btn_site = types.InlineKeyboardButton("На сайт", url=module["url"])
    btn_other = types.InlineKeyboardButton("Другой модуль", callback_data="choose_another")
    keyboard.add(btn_more, btn_site)
    keyboard.add(btn_other)

    bot.send_message(
        chat_id,
        text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )


# === Коллбэки ===
@bot.callback_query_handler(func=lambda call: call.data.startswith("more_"))
def show_details(call):
    key = call.data.replace("more_", "")
    module = MODULES_DB.get(key)
    if not module:
        bot.answer_callback_query(call.id, "Модуль не найден.")
        return

    full_text = (
        f"📘 Подробнее о модуле *{module['name']}*\n\n"
        f"*Категория:* {module['category']}\n"
        f"*Что решает:* {module['description']}\n\n"
        f"✅ Работает на вашем сервере\n"
        f"✅ Полный контроль над данными\n"
        f"✅ Интеграция с другими модулями Снег и ком"
    )

    keyboard = types.InlineKeyboardMarkup()
    btn_site = types.InlineKeyboardButton("Перейти на сайт", url=module["url"])
    btn_menu = types.InlineKeyboardButton("В меню", callback_data="main_menu")
    keyboard.add(btn_site)
    keyboard.add(btn_menu)

    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=full_text,
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"[Ошибка редактирования] {e}")


@bot.callback_query_handler(func=lambda call: call.data == "choose_another")
def back_to_pain(call):
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Какая боль сейчас сильнее?\n\n"
                 "1. Постоянно теряю данные\n"
                 "2. Всё делается вручную\n"
                 "3. Нет порядка в клиентах\n"
                 "4. Зависим от разработчиков\n"
                 "5. Не знаю, с чего начать\n\n"
                 "Напиши цифру.",
        )
        waiting_for_pain.add(call.message.chat.id)
    except Exception as e:
        print(f"[Ошибка] {e}")
