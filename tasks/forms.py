from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "deadline", "private"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "deadline": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "private": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
