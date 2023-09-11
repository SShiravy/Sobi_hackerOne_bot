import asyncio
from telegram import Bot
from config import TELEGRAM_TOKEN, CHAT_ID


def send_scopes(data_items):
    bot = Bot(token=TELEGRAM_TOKEN)
    # نمایش داده‌های جدید و جداول متناظر با آنها
    for table_name, data in data_items:
        if data:
            message = f"New Data for Table '{table_name}': {data}"
            print(message)

            # ارسال پیام به تلگرام
            loop = asyncio.get_event_loop()
            loop.run_until_complete(bot.send_message(chat_id=CHAT_ID, text=message))
