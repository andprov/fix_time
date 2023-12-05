from django.utils.datetime_safe import datetime
from django.utils.timezone import now

from apps.core.constants import DAY_END
from apps.dashboard.models import Time


class TimeProcessor:
    @staticmethod
    def get_timer(day, start, stop):
        diff = datetime.combine(day, stop) - datetime.combine(day, start)
        total_seconds = diff.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours:02.0f}:{minutes:02.0f}"

    @staticmethod
    def get_duration(day, start, stop):
        diff = datetime.combine(day, stop) - datetime.combine(day, start)
        total_seconds = diff.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        if minutes > 29:
            return hours + 1
        return hours

    def close_old_active_timer(self, user, data):
        active_timers = Time.objects.filter(user=user, stop=None)
        if active_timers:
            today = now().date()
            for timer in active_timers:
                if timer.day != today or (
                    data["day"] == today and data["stop"] is None
                ):
                    timer.stop = (
                        DAY_END if timer.day != today else now().time()
                    )
                    timer.duration = self.get_duration(
                        timer.day, timer.start, timer.stop
                    )
                    timer.save()

    def stop_active_timer(self, user):
        timer = Time.objects.filter(user=user, stop=None).first()
        if timer:
            timer.stop = now().time()
            timer.duration = self.get_duration(
                timer.day, timer.start, timer.stop
            )
            timer.save()
