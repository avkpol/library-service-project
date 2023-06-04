from django.db import models

class Book(models.Model):
    HARD = 'H'
    SOFT = 'S'
    COVER_CHOICES = [
        (HARD, 'Hardcover'),
        (SOFT, 'Softcover'),
    ]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=1, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title

