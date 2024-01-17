from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

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


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'task_description', 'status', 'project']
