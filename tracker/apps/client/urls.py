from django.urls import path

from apps.client.views import (
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
)

app_name = "client"

urlpatterns = [
    path(
        "",
        ClientListView.as_view(),
        name="list",
    ),
    path(
        "create/",
        ClientCreateView.as_view(),
        name="create",
    ),
    path(
        "<int:pk>/update/",
        ClientUpdateView.as_view(),
        name="update",
    ),
    path(
        "<int:pk>/delete/",
        ClientDeleteView.as_view(),
        name="delete",
    ),
]
