from . import views
from django.urls import path

urlpatterns = [
    path('', views.ProductList.as_view(), name='home'),
    path('<slug:slug>/', views.product_detail, name='product_detail')
]