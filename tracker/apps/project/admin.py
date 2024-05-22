from django.contrib import admin

from apps.project.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "client",
        "status",
        "amount",
        "payment_type",
    )
    search_fields = ("name",)
    list_filter = (
        "user",
        "client",
    )
