from django.db import models

from apps.client.models import Client
from apps.profile.models import User
from apps.core.constants import LENGTH_CHAR_FIELD


class StatusManager(models.Manager):
    def get_queryset(self):
        """Return QuerySet of projects with status=Active."""
        return (
            super()
            .get_queryset()
            .select_related("client")
            .filter(status=Project.Status.ACTIVE)
        )


class Project(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "Active", "Active"
        DONE = "Done", "Done"

    class Payment(models.TextChoices):
        HOUR = "Hour", "per hour"
        MONTH = "Month", "per month"

    name = models.CharField(
        verbose_name="Project Name",
        max_length=LENGTH_CHAR_FIELD,
    )
    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.CASCADE,
    )
    client = models.ForeignKey(
        Client,
        verbose_name="Client",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        db_index=True,
    )
    notes = models.TextField(
        verbose_name="Notes",
        blank=True,
    )
    status = models.CharField(
        verbose_name="Status",
        max_length=LENGTH_CHAR_FIELD,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    billing = models.BooleanField(
        verbose_name="Billing",
        default=False,
    )
    amount = models.PositiveIntegerField(
        verbose_name="Amount",
        blank=True,
        default=0,
    )
    payment_type = models.CharField(
        verbose_name="Payment type",
        max_length=LENGTH_CHAR_FIELD,
        choices=Payment.choices,
        default=Payment.HOUR,
    )

    objects = models.Manager()
    active = StatusManager()

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ("name",)

    def __str__(self):
        return self.name
