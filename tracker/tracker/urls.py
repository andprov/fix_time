from django.contrib import admin
from django.urls import path, include

from apps.profile import views


urlpatterns = [
    path("", include("apps.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("auth/signup/", views.UserCreateView.as_view(), name="signup"),
    path("admin/", admin.site.urls),
]
