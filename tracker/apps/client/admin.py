from django.contrib import admin

from apps.client.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
    )
    search_fields = ("name",)
    list_filter = ("user",)
