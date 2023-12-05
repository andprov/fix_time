from django.urls import path

from apps.project.views import (
    ProjectListView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDeleteView,
)

app_name = "project"

urlpatterns = [
    path("", ProjectListView.as_view(), name="list"),
    path("create/", ProjectCreateView.as_view(), name="create"),
    path("<int:pk>/update/", ProjectUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", ProjectDeleteView.as_view(), name="delete"),
]
