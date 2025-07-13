from . import views
from django.urls import path

urlpatterns = [
    path('', views.PerfilView.as_view(), name='perfil'),
]