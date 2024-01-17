from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistrationForm, ProjectForm, TaskForm
from .models import Project, Task


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project_list')
    else:
        form = RegistrationForm()
    return render(request, 'taskapp/register.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('project_list')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid input. Please correct the errors below.')
    else:
        form = AuthenticationForm()

    return render(request, 'taskapp/login.html', {'form': form})


def create_project(request):
    if request.method == "POST":
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'taskapp/create_project.html', {'form': form})


def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'taskapp/edit_project.html', {'form': form, 'project': project})


def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == 'POST':
        project.delete()
        return redirect('project_list')

    return render(request, 'taskapp/project_confirm_delete.html', {'project': project})


def project_list(request):
    projects = Project.objects.filter(user=request.user).order_by('-id')[:5]
    return render(request, 'taskapp/project_list.html', {'projects': projects})


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    tasks = Task.objects.filter(project=project).order_by('-created_at')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()

    return render(request, 'taskapp/project_detail.html', {'project': project, 'tasks': tasks, 'form': form})


def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.project = project
            task.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()
    return render(request, 'taskapp/create_task.html', {'form': form, 'project': project})


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=task.project.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'taskapp/edit_task.html', {'form': form, 'task': task})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('project_detail', project_id=task.project.id)

    return render(request, 'taskapp/task_confirm_delete.html', {'task': task})



