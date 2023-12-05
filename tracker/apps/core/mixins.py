from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect


class UserAccessMixin(LoginRequiredMixin):
    """Mixin to enforce user access control in views.

    This mixin requires the user to be authenticated. Additionally,
    it checks whether the user making the request has access to the object
    in question. If not, a 404 HTTP error is raised.
    """

    def dispatch(self, request, *args, **kwargs):
        """Checking user authentication and access to the object.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The HTTP response after processing the request.

        Raises:
            Http404: If the user is not authenticated or does not have access
            to the object.
        """
        if not request.user.is_authenticated:
            return redirect("login")
        if self.get_object().user != request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
