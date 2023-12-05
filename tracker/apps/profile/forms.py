from django.contrib.auth.forms import UserCreationForm
from django.forms import PasswordInput, TextInput, EmailInput, Form
from django.forms.models import ModelForm
from django.forms.fields import EmailField, CharField


from apps.profile.models import User
from apps.core.constants import LENGTH_EMAIL_FIELD


class RegistrationForm(UserCreationForm):
    username = CharField(
        label="username",
        widget=TextInput,
    )
    email = EmailField(
        label="email",
        widget=EmailInput,
    )
    password1 = CharField(
        label="password",
        widget=PasswordInput,
    )
    password2 = CharField(
        label="password confirmation",
        widget=PasswordInput,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class SentConfirmEmailForm(Form):
    email = EmailField(
        label="email",
        max_length=LENGTH_EMAIL_FIELD,
        widget=EmailInput,
    )


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
