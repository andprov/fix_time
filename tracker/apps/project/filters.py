from django_filters import CharFilter, FilterSet

from apps.project.models import Project


class ProjectFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Project
        fields = (
            "name",
            "status",
        )
