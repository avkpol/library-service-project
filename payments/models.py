from django.db import models
from enum import Enum
from django.urls import reverse


from book.models import Book
from borrowing.models import Borrowing


class PaymentStatus(Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'

class PaymentType(Enum):
    PAYMENT = 'PAYMENT'
    FINE = 'FINE'

class Payment(models.Model):
    status = models.CharField(max_length=10, choices=[(status.value, status.name) for status in PaymentStatus])
    type = models.CharField(max_length=10, choices=[(type.value, type.name) for type in PaymentType])
    borrowing = models.OneToOneField(Borrowing, on_delete=models.CASCADE)
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    to_pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    @property
    def money_to_pay(self):
        borrowing = Borrowing.objects.get(pk=self.borrowing_id)
        book = Book.objects.get(pk=borrowing.book_id)
        total_price = book.daily_fee * borrowing.duration_in_days()

        return total_price

    @money_to_pay.setter
    def money_to_pay(self, value):
        pass

    def __str__(self):
        return f"Payment #{self.pk}"

    # def get_absolute_url(self):
    #     return reverse('payment-detail', args=[str(self.pk)])

