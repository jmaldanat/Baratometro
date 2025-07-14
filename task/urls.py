from . import views
from django.urls import path

urlpatterns = [
    path('', views.TaskView.as_view(), name='task'),
    path('create-from-url/', views.create_task_from_url, name='create_task_from_url'),
]