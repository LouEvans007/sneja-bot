# config.py
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("Не задан TOKEN в .env")

MAIN_CHANNEL = "@snegikom"
PRIVATE_CHANNEL_LINK = "https://t.me/+L5FHukMqjvhiZWUy"
WEBSITE_URL = "https://snegikom.ru"
