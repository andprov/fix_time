from django.urls import path

from apps.profile.views import (
    ProfileView,
    SignUpDoneView,
    SendConfirmEmailView,
    ProfileUpdateView,
    ProfileDeleteView,
    UserEmailConfirmCompleteView,
)

app_name = "profile"

urlpatterns = [
    path(
        "",
        ProfileView.as_view(),
        name="profile",
    ),
    path(
        "send_confirm_email/",
        SendConfirmEmailView.as_view(),
        name="send_confirm_email",
    ),
    path(
        "sign_up_done/",
        SignUpDoneView.as_view(),
        name="sign_up_done",
    ),
    path(
        "email_confirm_complete/<uidb64>/<token>/",
        UserEmailConfirmCompleteView.as_view(),
        name="email_confirm_complete",
    ),
    path(
        "update/",
        ProfileUpdateView.as_view(),
        name="update",
    ),
    path(
        "delete/",
        ProfileDeleteView.as_view(),
        name="delete",
    ),
]
