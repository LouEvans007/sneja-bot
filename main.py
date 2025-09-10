# main.py
import telebot
from bot_instance import bot

# Просто импортируем — хэндлеры сами себя регистрируют
import handlers.start_handler
import handlers.menu_handler
import handlers.story_handler
import handlers.module_selector  # <-- автоматически добавляет свои обработчики

print("❄️ Снежа запущен. Ожидаю команд...")

if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"[КРИТИЧЕСКАЯ ОШИБКА] {e}")
