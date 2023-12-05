from django.forms import DateInput
from django.utils.timezone import now
from django_filters import FilterSet, DateFilter

from apps.dashboard.models import Time


class DashboardFilter(FilterSet):
    day = DateFilter(
        field_name="day",
        widget=DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "max": now().date(),
            }
        ),
        required=True,
    )

    class Meta:
        model = Time
        fields = ("day",)
