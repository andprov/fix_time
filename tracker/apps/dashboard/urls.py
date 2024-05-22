from django.urls import path

from apps.dashboard.views import (
    DashboardListView,
    DashboardCreateView,
    DashboardUpdateView,
    DashboardDeleteView,
)

app_name = "dashboard"

urlpatterns = [
    path(
        "",
        DashboardListView.as_view(),
        name="dashboard",
    ),
    path(
        "create/",
        DashboardCreateView.as_view(),
        name="create",
    ),
    path(
        "<int:pk>/update/",
        DashboardUpdateView.as_view(),
        name="update",
    ),
    path(
        "<int:pk>/delete/",
        DashboardDeleteView.as_view(),
        name="delete",
    ),
]
