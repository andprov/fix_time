from django.forms.models import ModelForm

from apps.client.models import Client


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ("name",)
