from django_filters import FilterSet, CharFilter

from apps.client.models import Client


class ClientFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        name = Client
        fields = ["name"]
