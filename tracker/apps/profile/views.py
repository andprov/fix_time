from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    FormView,
)

from apps.profile.forms import (
    RegistrationForm,
    ProfileUpdateForm,
    SentConfirmEmailForm,
)
from apps.profile.models import User
from apps.profile.services.processor import AccountActivator


class SendConfirmEmailMixin:
    """Mixin to handle sending confirmation emails.

    Attributes:
        None

    Methods:
        send_confirm_url(self, email):
            Sends a confirmation email to the provided email address.

        get_confirm_url(self):
            Generates and returns the confirmation URL.

    Note:
        This mixin should be used in views that require sending
        confirmation emails.
    """

    def send_confirm_url(self, email):
        """Sends a confirmation email to the provided email address.

        Args:
            email (str): The recipient's email address.
        """
        confirm_url = self.get_confirm_url()
        send_mail(
            subject="Confirm email address.",
            message=(
                f"Follow the link to activate your account.\n{confirm_url}"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=True,
        )

    def get_confirm_url(self):
        """Generates and returns the confirmation URL.

        Returns:
            str: The confirmation URL.
        """
        domain = get_current_site(self.request).domain
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        confirm_url = reverse(
            "profile:email_confirm_complete", args=[uidb64, token]
        )
        return f"{domain}{confirm_url}"


class UserCreateView(SendConfirmEmailMixin, CreateView):
    """View for user registration and sending confirmation email.

    Attributes:
        form_class (Form): The form class for user registration.
        model (Model): The model for which the view is created (User).
        template_name (str): The name of the template to be rendered.
        success_url (str): The URL to redirect to after a successful operation.

    Methods:
        form_valid(self, form):
            Processes the form when it is valid.
    """

    form_class = RegistrationForm
    model = User
    template_name = "registration/signup.html"
    success_url = reverse_lazy("profile:sign_up_done")

    def form_valid(self, form):
        """Processes the form when it is valid.

        Args:
            form (Form): The valid form instance.

        Returns:
            HttpResponse: The HTTP response after successful form processing.
        """
        response = super().form_valid(form)
        self.object.is_active = False
        self.user = form.save()
        self.send_confirm_url(self.user.email)
        return response


class SendConfirmEmailView(SendConfirmEmailMixin, FormView):
    """View for sending a confirmation email.

    Attributes:
        form_class (Form): The form class for sending confirmation emails.
        template_name (str): The name of the template to be rendered.
        success_url (str): The URL to redirect to after a successful operation.

    Methods:
        form_valid(self, form):
            Processes the form when it is valid.
    """

    form_class = SentConfirmEmailForm
    template_name = "profile/signup_send_email.html"
    success_url = reverse_lazy("profile:sign_up_done")

    def form_valid(self, form):
        """Processes the form when it is valid.

        Args:
            form (Form): The valid form instance.

        Returns:
            HttpResponse: The HTTP response after successful form processing.
        """
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")
        self.user = User.objects.filter(email=email).first()
        if self.user:
            self.send_confirm_url(email)
            return response
        form.add_error("email", "The user with this email not registered")
        return self.form_invalid(form)


class SignUpDoneView(TemplateView):
    """View for displaying a message after successful user registration.

    Attributes:
        template_name (str): The name of the template to be rendered.
    """

    template_name = "profile/sign_up_done.html"


class UserEmailConfirmCompleteView(View):
    """View for completing email confirmation.

    Attributes:
        http_method_names (list): The allowed HTTP methods (GET).
        template_name (str): The name of the template to be rendered.
        success_url (str): The URL to redirect to after a successful operation.
    """

    http_method_names = ["get"]
    template_name = "profile/email_confirm_complete.html"
    success_url = reverse_lazy("profile:sign_up_done")

    def dispatch(self, request, **kwargs):
        """Handles the dispatch of the view.

        Args:
            request (HttpRequest): The HTTP request object.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response after processing the request.
        """
        uidb64, token = kwargs.get("uidb64"), kwargs.get("token")
        context = {"valid_url": AccountActivator().execute(uidb64, token)}
        return render(request, self.template_name, context)


class ProfileView(LoginRequiredMixin, DetailView):
    """View for displaying user profile details.

    Attributes:
        model (Model): The model for which the view is created (User).
        template_name (str): The name of the template to be rendered.

    Methods:
        get_object(self, queryset=None):
            Returns the user object for the logged-in user.
    """

    model = User
    template_name = "profile/profile.html"

    def get_object(self, queryset=None):
        """Returns user object for the logged-in user.

        Args:
            queryset (QuerySet): The queryset to be used.

        Returns:
            User: The user object.
        """
        return self.request.user


class ProfileUpdateView(ProfileView, UpdateView):
    """View for updating user profile details.

    Attributes:
        form_class (Form): The form class for updating user profile details.
        template_name (str): The name of the template to be rendered.
        success_url (str): The URL to redirect to after a successful operation.
    """

    form_class = ProfileUpdateForm
    template_name = "profile/update.html"
    success_url = reverse_lazy("profile:profile")


class ProfileDeleteView(ProfileView, DeleteView):
    """View for deleting user profile.

    Attributes:
        template_name (str): The name of the template to be rendered.
        success_url (str): The URL to redirect to after a successful operation.
    """

    template_name = "profile/delete.html"
    success_url = reverse_lazy("home:frontpage")
