import os

from dotenv import load_dotenv

# Загружаем переменные из файла .env (он не попадает в git)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///calendar.db")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "15"))  # секунды между проверками

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError(
        "Не заданы BOT_TOKEN или CHAT_ID. Скопируйте .env.example в .env и заполните его."
    )
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
