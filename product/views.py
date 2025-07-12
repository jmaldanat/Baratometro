from django.shortcuts import render
from django.views import generic
from .models import ProductPrice

# Create your views here.

class ProductList(generic.ListView):
    # Obtiene el precio más bajo para cada producto (versión para PostgreSQL)
    queryset = ProductPrice.objects.order_by('product_id', 'price').distinct('product_id')
    template_name = "product/newindex.html"
    #paginate_by = 4  # Número de productos por página