from django.urls import path, include


urlpatterns = [
    path("", include("apps.home.urls", namespace="home")),
    path("client/", include("apps.client.urls", namespace="client")),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
    path("profile/", include("apps.profile.urls", namespace="profile")),
    path("project/", include("apps.project.urls", namespace="project")),
    path("report/", include("apps.report.urls", namespace="report")),
]
