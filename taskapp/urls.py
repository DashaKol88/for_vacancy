from django.urls import path

from . import views

urlpatterns =[path('register/', views.register, name='register'),
              path('login/', views.login_user, name='login'),
              path('projects/create/', views.create_project, name='create_project'),
              path('projects/edit/<int:project_id>/', views.edit_project, name='edit_project'),
              path('projects/delete/<int:project_id>/', views.delete_project, name='delete_project'),
              path('projects/', views.project_list, name='project_list'),
              ]