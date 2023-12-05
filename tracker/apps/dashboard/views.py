from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from apps.core.constants import CREATE, UPDATE, DELETE
from apps.core.mixins import UserAccessMixin
from apps.dashboard.filters import DashboardFilter
from apps.dashboard.forms import TimeForm
from apps.dashboard.models import Time
from apps.dashboard.services.processor import TimeProcessor
from apps.project.models import Project


TITLE = "Time Entry"
DASHBOARD = "dashboard:dashboard"
DELETE_LINK = "dashboard:delete"


class DashboardListView(LoginRequiredMixin, FilterView):
    """View for displaying a paginated list of time entries in the dashboard.

    Attributes:
        model (Model): The model for which the view is created (Time).
        filterset_class (Filter Set): The filter set class for dashboard
        filtering.
        template_name (str): The name of the template to be rendered.
        paginate_by (int): Number of time entries to display per page.

    Methods:
        get_queryset(self): Returns the queryset of time entries associated
        with the logged-in user.
        get_context_data(self, **kwargs): Returns the context data for
        rendering the template.
        get(self, request, *args, **kwargs): Handles GET requests for
        navigating through time entries.
        post(self, request, *args, **kwargs): Handles POST requests to stop
        the active timer and redirect to the dashboard.
    """

    model = Time
    filterset_class = DashboardFilter
    template_name = "dashboard/dashboard.html"
    paginate_by = 20

    def get_queryset(self):
        """Returns the queryset of time entries associated with the logged-in
        user.
        """
        self.queryset = (
            Time.objects.filter(user=self.request.user)
            .select_related("project")
            .order_by("start")
        )
        return self.queryset

    def get_context_data(self, **kwargs):
        """Returns the context data for rendering the template."""
        context = super().get_context_data(**kwargs)
        active_timer = self.queryset.filter(stop=None).first()
        if active_timer:
            context.update(
                {
                    "active_timer": True,
                    "active_timer_duration": TimeProcessor().get_timer(
                        active_timer.day,
                        active_timer.start,
                        now().time(),
                    ),
                }
            )
        return context

    def get(self, request, *args, **kwargs):
        """Handles GET requests for navigating through time entries.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response after processing the request.
        """
        date_str = request.GET.get("day", now().date().strftime("%Y-%m-%d"))
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        direction = request.GET.get("direction")
        if direction == "backward":
            selected_date -= timedelta(days=1)
        elif direction == "forward" and selected_date != now().date():
            selected_date += timedelta(days=1)
        request.GET = request.GET.copy()
        request.GET["day"] = selected_date.strftime("%Y-%m-%d")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handles POST requests to stop the active timer and redirect
        to the dashboard.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response after processing the request.
        """
        TimeProcessor().stop_active_timer(self.request.user)
        return redirect(DASHBOARD)


class DashboardView:
    """Base view for time entry-related operations.

    Attributes:
        model (Model): The model for which the view is created (Time).
        template_name (str): The name of the template to be rendered.
        success_url (str): The URL to redirect to after a successful operation.
    """

    model = Time
    template_name = "include/edit.html"
    success_url = reverse_lazy(DASHBOARD)


class DashboardCreateView(DashboardView, LoginRequiredMixin, CreateView):
    """View for creating a new time entry.

    Attributes:
        form_class (Form): The form class for time entry creation.

    Methods:
        get_form_fields(self, form): Updates form fields based on user and
        current time.
        get_form(self, form_class=None): Returns the form instance with
        updated fields.
        form_valid(self, form): Processes the form when it is valid.
        get_context_data(self, **kwargs): Returns the context data for
        rendering the template.
    """

    form_class = TimeForm

    def get_form_fields(self, form):
        """Updates form fields based on user and current time."""
        form.fields["project"].queryset = Project.active.filter(
            user=self.request.user, payment_type=Project.Payment.HOUR
        )
        form.fields["day"].initial = now().strftime("%Y-%m-%d")
        form.fields["start"].initial = now().strftime("%H:%M")

    def get_form(self, form_class=None):
        """Returns the form instance with updated fields."""
        form = super().get_form(form_class)
        self.get_form_fields(form)
        return form

    def form_valid(self, form):
        """Processes the form when it is valid.

        Args:
            form (Form): The valid form instance.

        Returns:
            HttpResponse: The HTTP response after successful form processing.
        """
        form.instance.user = self.request.user
        data = form.cleaned_data
        TimeProcessor().close_old_active_timer(self.request.user, data)
        if data["stop"]:
            form.instance.duration = TimeProcessor().get_duration(
                data["day"], data["start"], data["stop"]
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Returns the context data for rendering the template."""
        context = super().get_context_data()
        context.update(
            {
                "title": TITLE,
                "action": CREATE,
                "back_link": DASHBOARD,
            }
        )
        return context


class DashboardUpdateView(DashboardCreateView, UserAccessMixin, UpdateView):
    """View for updating an existing time entry.

    Methods:
        get_context_data(self, **kwargs): Returns the context data for
        rendering the template.
    """

    def get_context_data(self, **kwargs):
        """Returns the context data for rendering the template."""
        context = super().get_context_data()
        context.update(
            {
                "action": UPDATE,
                "delete_link": DELETE_LINK,
                "pk": self.kwargs.get("pk"),
            }
        )
        return context


class DashboardDeleteView(DashboardView, UserAccessMixin, DeleteView):
    """View for deleting an existing time entry.

    Methods:
        get_context_data(self, **kwargs): Returns the context data for
        rendering the template.
    """
    def get_context_data(self, **kwargs):
        """Returns the context data for rendering the template."""
        context = super().get_context_data()
        context.update(
            {
                "title": TITLE,
                "action": DELETE,
                "back_link": DASHBOARD,
            }
        )
        return context
