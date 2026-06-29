from django import forms
from myApp.models import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ("posted_by",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} form-control".strip()
    