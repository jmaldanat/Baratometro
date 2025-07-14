from . import views
from django.urls import path

urlpatterns = [
    path('', views.PerfilView.as_view(), name='perfil'),
    path('account/', views.AccountSettingsView.as_view(), name='profile_account'),
]