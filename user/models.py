from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Customer(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name="customers",
        blank=True,
        help_text="The groups this customer belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customers",
        blank=True,
        help_text="Specific permissions for this customer.",
        verbose_name="user permissions",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.email
