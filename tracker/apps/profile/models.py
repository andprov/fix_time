from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.core.constants import LENGTH_EMAIL_FIELD


class User(AbstractUser):
    email = models.EmailField(
        verbose_name="email",
        max_length=LENGTH_EMAIL_FIELD,
        unique=True,
    )

    class Meta:
        ordering = ("username",)

    def __str__(self):
        return self.username
