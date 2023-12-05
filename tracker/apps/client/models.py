from django.db import models

from apps.profile.models import User
from apps.core.constants import LENGTH_CHAR_FIELD


class Client(models.Model):
    name = models.CharField(
        verbose_name="Client Name",
        max_length=LENGTH_CHAR_FIELD,
    )
    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ("name",)

    def __str__(self):
        return self.name
