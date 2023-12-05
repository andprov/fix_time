from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from apps.project.filters import ProjectFilter
from apps.project.forms import ProjectForm
from apps.core.constants import CREATE, DELETE, UPDATE
from apps.project.models import Project
from apps.core.mixins import UserAccessMixin

TITLE = "Project"
PROJECT_LIST = "project:list"
DELETE_LINK = "project:delete"


class ProjectListView(LoginRequiredMixin, FilterView):
    """View for displaying a paginated list of projects associated with the
    logged-in user.

    Attributes:
        model (Model): The model for which the view is created (Project).
        filterset_class (FilterSet): The filter set class for project
        filtering.
        template_name (str): The name of the template to be rendered.
        paginate_by (int): Number of projects to display per page.

    Methods:
        get_queryset(self): Returns the queryset of projects associated with
        the logged-in user.
        get_filterset_kwargs(self, filterset_class): Returns the keyword
        arguments for instantiating the filter set.
        get_context_data(self, **kwargs): Returns the context data for
        rendering the template.
    """

    model = Project
    filterset_class = ProjectFilter
    template_name = "project/list.html"
    paginate_by = 10

    def get_queryset(self):
        """Returns queryset of projects associated with the logged-in user."""
        return (
            Project.objects.all()
            .select_related("client")
            .filter(user=self.request.user)
        )

    def get_filterset_kwargs(self, filterset_class):
        """Returns the keyword arguments for instantiating the filter set.

        Args:
            filterset_class (FilterSet): The filter set class.
        """
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs["data"] = self.request.GET.copy()
        if "status" not in kwargs["data"]:
            kwargs["data"]["status"] = Project.Status.ACTIVE
        return kwargs

    def get_context_data(self, **kwargs):
        """Returns the context data for rendering the template."""
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        if "page" in query_params:
            del query_params["page"]
        context["urlencode"] = query_params.urlencode()
        return context


class ProjectView:
    """Base view for project-related operations.

    Attributes:
        model (Model): The model for which the view is created (Project).
        template_name (str): The name of the template to be rendered.
        success_url (str): The URL to redirect to after a successful operation.
    """

    model = Project
    template_name = "include/edit.html"
    success_url = reverse_lazy(PROJECT_LIST)


class ProjectCreateView(ProjectView, LoginRequiredMixin, CreateView):
    """View for creating a new project.

    Attributes:
        form_class (Form): The form class for project creation.

    Methods:
        get_form(self, form_class=None): Returns the form instance with
        updated fields.
        form_valid(self, form): Processes the form when it is valid.
        get_context_data(self, **kwargs): Returns the context data for
        rendering the template.
    """

    form_class = ProjectForm

    def get_form(self, form_class=None):
        """Returns the form instance with updated fields.

        Args:
            form_class (Form): The form class.
        """
        form = super().get_form(form_class)
        form.fields["client"].queryset = self.request.user.client_set.all()
        return form

    def form_valid(self, form):
        """Processes the form when it is valid.

        Args:
            form (Form): The valid form instance.

        Returns:
            HttpResponse: The HTTP response after successful form processing.
        """
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Returns the context data for rendering the template."""
        context = super().get_context_data()
        context.update(
            {
                "title": TITLE,
                "action": CREATE,
                "back_link": PROJECT_LIST,
            }
        )
        return context


class ProjectUpdateView(ProjectCreateView, UserAccessMixin, UpdateView):
    """View for updating an existing project.

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


class ProjectDeleteView(ProjectView, UserAccessMixin, DeleteView):
    """View for deleting an existing project.

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
                "back_link": PROJECT_LIST,
                "name": self.object.name,
            }
        )
        return context
