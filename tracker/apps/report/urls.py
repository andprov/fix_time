from django.urls import path

from apps.report.views import ReportsListView

app_name = "report"

urlpatterns = [
    path(
        "",
        ReportsListView.as_view(),
        name="report",
    ),
]
