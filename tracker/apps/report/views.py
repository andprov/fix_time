from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django_filters.views import FilterView

from apps.client.models import Client
from apps.dashboard.models import Time
from apps.project.models import Project
from apps.report.filters import ReportFilter


class ReportsListView(LoginRequiredMixin, FilterView):
    """View for generating and displaying time-related reports.

    Attributes:
        model (Model): The model for which the view is created (Time).
        filterset_class (FilterSet): The filter set class for report filtering.
        template_name (str): The name of the template to be rendered.
        request (HttpRequest): The HTTP request object.

    Methods:
        get_queryset(self): Returns the queryset of time entries based on
        applied filters.
        get_context_data(self, **kwargs): Returns the context data for
        rendering the template.
    """

    model = Time
    filterset_class = ReportFilter
    template_name = "report/report.html"
    request = None

    def get_queryset(self):
        """Returns the queryset of time entries based on applied filters."""
        user = self.request.user
        self.queryset = Time.objects.none()
        self.filterset_class.base_filters[
            "project"
        ].queryset = Project.objects.filter(
            user=self.request.user, payment_type=Project.Payment.HOUR
        )
        self.filterset_class.base_filters[
            "project__client"
        ].queryset = Client.objects.filter(user=self.request.user)

        if self.request.GET:
            self.queryset = self.filterset_class(
                self.request.GET,
                queryset=Time.objects.filter(
                    user=user,
                    stop__isnull=False,
                ).select_related("project"),
            ).qs
        return self.queryset

    def get_context_data(self, **kwargs):
        """Returns the context data for rendering the template."""
        context = super().get_context_data(**kwargs)
        total_duration = ""
        if self.queryset:
            total_duration = self.queryset.aggregate(Sum("duration"))[
                "duration__sum"
            ]
        context.update({"total_duration": total_duration})
        return context
