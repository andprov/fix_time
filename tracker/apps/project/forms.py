from django.forms import ModelForm, Textarea

from apps.core.constants import MAX_AMOUNT
from apps.project.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        exclude = ("user",)
        widgets = {
            "notes": Textarea({"rows": "2"}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")
        if amount is None:
            amount = 0
        elif amount > MAX_AMOUNT:
            amount = MAX_AMOUNT
        return amount
