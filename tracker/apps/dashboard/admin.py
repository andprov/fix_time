from django.contrib import admin

from apps.dashboard.models import Time


@admin.register(Time)
class TimeAdmin(admin.ModelAdmin):
    ...
