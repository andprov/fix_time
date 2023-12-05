from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from apps.client.filters import ClientFilter
from apps.client.forms import ClientForm
from apps.client.models import Client
from apps.core.constants import CREATE, UPDATE, DELETE
from apps.core.mixins import UserAccessMixin


TITLE = "Client"
CLIENT_LIST = "client:list"
DELETE_LINK = "client:delete"


class ClientListView(LoginRequiredMixin, FilterView):
    """View for displaying a paginated list of clients associated with the
    logged-in user.

    Attributes:
        model (Model): The model for which the view is created (Client).
        filter set_class (Filter Set): The filter set class for client
        filtering.
        template_name (str): The name of the template to be rendered.
        paginate_by (int): Number of clients to display per page.

    Methods:
        get_queryset(self): Returns the queryset of clients associated with
        the logged-in user.
    """

    model = Client
    filterset_class = ClientFilter
    template_name = "client/list.html"
    paginate_by = 10

    def get_queryset(self):
        """Returns queryset of clients associated with the logged-in user."""
        user = self.request.user
        queryset = user.client_set.all()
        return queryset


class ClientView:
    """Base view for client-related operations.

    Attributes:
        model (Model): The model for which the view is created (Client).
        template_name (str): The name of the template to be rendered.
        success_url (str): The URL to redirect to after a successful operation.
    """

    model = Client
    template_name = "include/edit.html"
    success_url = reverse_lazy(CLIENT_LIST)


class ClientCreateView(ClientView, LoginRequiredMixin, CreateView):
    """View for creating a new client.

    Attributes:
        form_class (Form): The form class for client creation.

    Methods:
        form_valid(self, form): Processes the form when it is valid.
        get_context_data(self, **kwargs): Returns the context data for
        rendering the template.
    """

    form_class = ClientForm

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
                "back_link": CLIENT_LIST,
            }
        )
        return context


class ClientUpdateView(ClientCreateView, UserAccessMixin, UpdateView):
    """View for updating an existing client.

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


class ClientDeleteView(ClientView, UserAccessMixin, DeleteView):
    """View for deleting an existing client.

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
                "back_link": CLIENT_LIST,
                "name": self.object.name,
            }
        )
        return context
