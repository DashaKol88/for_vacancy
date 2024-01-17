from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=50)
    project_description = models.TextField(blank=True)
    deadline = models.DateField(blank=True, null=True, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [('new', 'New'), ('in_progress', 'In progress'), ('completed', 'Completed')]
    title = models.CharField(max_length=50)
    task_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title
