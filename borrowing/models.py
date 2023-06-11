from django.db import models

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(null=True, blank=False)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=False)
    book_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()


    def __str__(self):
        return f"Borrowing #{self.pk}"
