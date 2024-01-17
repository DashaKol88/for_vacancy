from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Project, Task


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'project_description', 'deadline']

    def clean_deadline(self):
        """
        Clean and validate the 'deadline' field.

        Returns:
        - datetime.date: The cleaned 'deadline'.
        """
        deadline = self.cleaned_data['deadline']

        # Check if the deadline is in the past
        if deadline and deadline < timezone.now().date():
            raise forms.ValidationError("Deadline cannot be in the past.")

        return deadline


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'task_description', 'status']
