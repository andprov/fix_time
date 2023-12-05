from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import DateField
from django.utils.timezone import now

from apps.core.constants import LENGTH_STR
from apps.project.models import Project
from apps.profile.models import User


def get_current_date():
    return now().date()


class Time(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="User",
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        Project,
        verbose_name="Project",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Description",
        blank=True,
        null=True,
    )
    day = DateField(
        verbose_name="Day",
        validators=[MaxValueValidator(get_current_date)],
    )
    start = models.TimeField(
        verbose_name="Start Time",
    )
    stop = models.TimeField(
        verbose_name="Stop Time",
        blank=True,
        null=True,
    )
    duration = models.PositiveSmallIntegerField(
        verbose_name="Duration",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Time"
        verbose_name_plural = "Time"
        ordering = ("day",)

    def __str__(self):
        return self.description[:LENGTH_STR]
