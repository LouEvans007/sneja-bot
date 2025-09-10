# utils/subscription.py
from bot_instance import bot
from config import MAIN_CHANNEL

def is_subscribed(chat_id):
    """
    Проверяет, подписан ли пользователь на основной канал.
    """
    try:
        member = bot.get_chat_member(MAIN_CHANNEL, chat_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"[Ошибка подписки] {e}")
        return False
