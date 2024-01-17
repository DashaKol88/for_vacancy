from django.contrib import admin
from .models import Project, Task


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'status', 'user', 'project')
    list_filter = ('status', 'user', 'project')
