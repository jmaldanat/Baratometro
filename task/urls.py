from . import views
from django.urls import path

urlpatterns = [
    path('', views.TaskView.as_view(), name='task'),
]