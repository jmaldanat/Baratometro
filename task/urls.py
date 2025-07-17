from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskView.as_view(), name='task'),
    path('create-from-url/', views.create_task_from_url, name='create_task_from_url'),
    path('status/', views.user_tasks_status, name='user_tasks_status'),
]