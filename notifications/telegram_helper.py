import os

import telegram

from django.db.models.signals import post_save
from django.dispatch import receiver

from borrowing.models import Borrowing


def send_telegram_message(chat_id, message):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    bot = telegram.Bot(token=bot_token)
    bot.sendMessage(chat_id=chat_id, text=message)

@receiver(post_save, sender=Borrowing)
def send_borrowing_notification(sender, instance, created, **kwargs):
    if created:
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        message = (
            f"New borrowing created!\nBorrowing ID: {instance.id}\n"
            f"User ID: {instance.user_id}\nBook ID: {instance.book_id}"
        )
        send_telegram_message(chat_id, message)

