import json
import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from borrowing.models import Borrowing



@receiver(post_save, sender=Borrowing)
def send_borrowing_notification(sender, instance, created, **kwargs):
    if created:
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        message = (
            f"New borrowing created!\nBorrowing ID: {instance.id}"
            f"\nUser ID: {instance.user_id}"
            f"\nBook ID: {instance.book_id}"
        )
        # send_telegram_message(chat_id, message)
        return json.dumps({'chat_id': chat_id, 'message': message})
