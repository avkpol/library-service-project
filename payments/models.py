from django.db import models
from enum import Enum
import math


from book.models import Book
from borrowing.models import Borrowing


class PaymentStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELED = 'CANCELED', 'Canceled'

class PaymentType(models.TextChoices):
    CARD = 'CARD', 'Card'
    CASH = 'CASH', 'Cash'

class Payment(models.Model):
    status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    type = models.CharField(max_length=10, choices=PaymentType.choices)
    borrowing = models.OneToOneField(Borrowing, null=True, on_delete=models.CASCADE)
    session_url = models.URLField(null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    to_pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    @property
    def money_to_pay(self):
        borrowing = Borrowing.objects.get(pk=self.borrowing_id)
        book = Book.objects.get(pk=borrowing.book_id)
        total_price = book.daily_fee * math.trunc((borrowing.actual_return_date - borrowing.borrow_date).days)

        return total_price

    @money_to_pay.setter
    def money_to_pay(self, value):
        pass

    def __str__(self):
        return f"Payment #{self.pk}"

    # def get_absolute_url(self):
    #     return reverse('payment-detail', args=[str(self.pk)])

