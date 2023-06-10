import os

import requests as requests
from asgiref.sync import async_to_sync
from borrowing.signals import send_borrowing_notification
import telegram

from django.db.models.signals import post_save
from django.dispatch import receiver

import borrowing
from borrowing.models import Borrowing
#
# borrowin = Borrowing
# message = (
#        f"New borrowing created!\nBorrowing ID: "f"{borrowin.id}"
#        f"\nUser ID: {borrowin.user_id}"
#        f"\nBook ID: {borrowin.book_id}"
# )

def send_telegram_message(*args, **kwargs):
    message = send_borrowing_notification()
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    telegram_api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    try:
        response = requests.post(telegram_api_url, json={'chat_id': chat_id, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)



def send_telegram_message(chat_id, message):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    try:
        response = requests.post(telegram_api_url, json={'chat_id': chat_id, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)



#
# @receiver(post_save, sender=Borrowing)
# def send_borrowing_notification(sender, instance, created, **kwargs):
#     if created:
#         chat_id = os.getenv('TELEGRAM_CHAT_ID')
#         message = (
#             f"New borrowing created!\nBorrowing ID: "f"{instance.id}"
#             f"\nUser ID: {instance.user_id}"
#             f"\nBook ID: {instance.book_id}"
#         )
#
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#
#         try:
#             loop.run_until_complete(send_telegram_message(chat_id, message))
#         finally:
#             loop.close()
#             asyncio.set_event_loop(None)

# def send_telegram_message(chat_id, message):
#     bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
#     bot = telegram.Bot(token=bot_token)
#     bot.send_message(chat_id=chat_id, text=message)
#
# @receiver(post_save, sender=Borrowing)
# def send_borrowing_notification(sender, instance, created, **kwargs):
#     if created:
#         chat_id = os.getenv('TELEGRAM_CHAT_ID')
#         message = (
#             f"New borrowing created!\nBorrowing ID: {instance.id}\n"
#             f"User ID: {instance.user_id}\nBook ID: {instance.book_id}"
#         )
#         send_telegram_message(chat_id, message)
