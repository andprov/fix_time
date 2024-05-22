from django.utils.timezone import now
from django_filters import (
    FilterSet,
    DateFromToRangeFilter,
)
from django_filters.widgets import RangeWidget

from apps.dashboard.models import Time


class ReportFilter(FilterSet):
    day = DateFromToRangeFilter(
        widget=RangeWidget(
            attrs={
                "type": "date",
                "max": now().date(),
            }
        ),
        required=True,
    )

    class Meta:
        model = Time
        fields = (
            "day",
            "project__client",
            "project",
        )
