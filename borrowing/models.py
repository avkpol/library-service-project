from django.db import models

from book.models import Book
from user.models import Customer


class Borrowing(models.Model):
    borrow_date = models.DateField(null=True, blank=False)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=False)
    book = models.ForeignKey(Book, default=1, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return f"Borrowing #{self.pk}"



