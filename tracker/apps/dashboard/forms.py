from django.forms import Textarea, DateInput, TimeInput
from django.forms.models import ModelForm
from django.utils.timezone import now

from apps.dashboard.models import Time


class TimeForm(ModelForm):
    class Meta:
        model = Time
        fields = ("day", "start", "stop", "project", "description")
        widgets = {
            "description": Textarea({"rows": "2"}),
            "day": DateInput(
                format="%Y-%m-%d", attrs={"type": "date", "max": now().date()}
            ),
            "start": TimeInput(format="%H:%M", attrs={"type": "time"}),
            "stop": TimeInput(format="%H:%M", attrs={"type": "time"}),
        }

    def _check_date_today(self):
        if self.day != now().date() and self.stop is None:
            self.add_error(
                "stop",
                "If date is not today then the end time should be filled in.",
            )

    def _check_start_stop(self):
        if self.stop and self.start > self.stop:
            self.add_error(
                "stop",
                "The stop time cannot be less than the start time.",
            )

    def _check_start_time(self):
        if self.day == now().date() and self.start > now().time():
            self.add_error(
                "start",
                "The start time cannot be greater than the current one.",
            )

    def _check_stop_time(self):
        if self.stop and self.day == now().date() and self.stop > now().time():
            self.add_error(
                "stop",
                "The stop time cannot be greater than the current one.",
            )

    def clean(self):
        cleaned_data = super().clean()
        self.day = cleaned_data.get("day")
        self.start = cleaned_data.get("start")
        self.stop = cleaned_data.get("stop")
        self._check_date_today()
        self._check_start_stop()
        self._check_start_time()
        self._check_stop_time()
        return cleaned_data
