from django import forms
from .models import Project, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "deadline", "private"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "deadline": forms.DateInput(attrs={
                "type": "date"},
                format="%Y-%m-%d"),
            "private": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "description",
            "deadline",
            "done",
            "time",
            "area",
        ]
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe the task..."
                }
            ),
            "deadline": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
                format="%Y-%m-%d",
            ),
            "time": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),
            "area": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["deadline"].input_formats = ["%Y-%m-%d"]
