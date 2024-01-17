from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistrationForm, ProjectForm, TaskForm
from .models import Project, Task


def register(request: HttpRequest) -> HttpResponse:
    """
    View for user registration.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response.
    """
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project_list')
    else:
        form = RegistrationForm()
    return render(request, 'taskapp/register.html', {'form': form})


def login_user(request: HttpRequest) -> HttpResponse:
    """
    View for user login.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response.
    """
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


def create_project(request: HttpRequest) -> HttpResponse:
    """
    View for creating a new project.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response.
    """
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


def edit_project(request: HttpRequest, project_id: int) -> HttpResponse:
    """
    View for editing an existing project.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - project_id (int): The ID of the project to be edited.

    Returns:
    - HttpResponse: The HTTP response.
    """
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)

    return render(request, 'taskapp/edit_project.html', {'form': form, 'project': project})


def delete_project(request: HttpRequest, project_id: int) -> HttpResponse:
    """
    View for confirming and deleting a project.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - project_id (int): The ID of the project to be deleted.

    Returns:
    - HttpResponse: The HTTP response.
    """
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if request.method == 'POST':
        project.delete()
        return redirect('project_list')

    return render(request, 'taskapp/project_confirm_delete.html', {'project': project})


def project_list(request: HttpRequest) -> HttpResponse:
    """
    View for listing user's projects.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response.
    """
    projects = Project.objects.filter(user=request.user).order_by('-id')[:5]
    return render(request, 'taskapp/project_list.html', {'projects': projects})


def project_detail(request: HttpRequest, project_id: int) -> HttpResponse:
    """
    View for displaying project details and handling task creation.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - project_id (int): The ID of the project.

    Returns:
    - HttpResponse: The HTTP response.
    """
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


def create_task(request: HttpRequest, project_id: int) -> HttpResponse:
    """
    View for creating a new task for a specific project.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - project_id (int): The ID of the project.

    Returns:
    - HttpResponse: The HTTP response.
    """
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


def edit_task(request: HttpRequest, task_id: int) -> HttpResponse:
    """
    View for editing an existing task.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - task_id (int): The ID of the task.

    Returns:
    - HttpResponse: The HTTP response.
    """
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', project_id=task.project.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'taskapp/edit_task.html', {'form': form, 'task': task})


def delete_task(request: HttpRequest, task_id: int) -> HttpResponse:
    """
    View for deleting an existing task.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - task_id (int): The ID of the task.

    Returns:
    - HttpResponse: The HTTP response.
    """
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('project_detail', project_id=task.project.id)

    return render(request, 'taskapp/task_confirm_delete.html', {'task': task})
