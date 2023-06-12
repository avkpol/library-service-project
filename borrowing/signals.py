import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.telegram_helper import send_telegram_message

from borrowing.models import Borrowing



@receiver(post_save, sender=Borrowing)
def send_borrowing_notification(sender, instance, created, **kwargs):
    if created:
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        message = (
            f"New borrowing created!\nBorrowing ID: "f"{instance.id}"
            f"\nUser ID: {instance.user_id}"
            f"\nBook ID: {instance.book_id}"
        )
        send_telegram_message(chat_id, message)