import os
import requests as requests
from notifications.signals import send_borrowing_notification

message = send_borrowing_notification


def send_telegram_message(chat_id, message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    try:
        response = requests.post(
            telegram_api_url, json={"chat_id": chat_id, "text": message}
        )
        print(response.text)
    except Exception as e:
        print(e)
