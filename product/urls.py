from . import views
from django.urls import path

urlpatterns = [
    path('', views.ProductList.as_view(), name='home'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('save/<int:product_id>/', views.save_product, name='save_product'),
    path('unsave/<int:product_id>/', views.unsave_product, name='unsave_product'),
    path('alert/<int:product_id>/', views.create_product_alert, name='create_product_alert'),  # <-- Añade esta línea
    path('delete-alert/<int:alert_id>/', views.delete_product_alert, name='delete_product_alert'),
]