from . import views
from django.urls import path
from .views import AlertsView

urlpatterns = [
    path('', views.PerfilView.as_view(), name='perfil'),
    path('account/', views.AccountSettingsView.as_view(), name='profile_account'),
    path('delete-account/', views.DeleteAccountView.as_view(), name='delete_account'),
    path('alerts/', AlertsView.as_view(), name='alerts'),
]