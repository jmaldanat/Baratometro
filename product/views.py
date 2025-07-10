from django.shortcuts import render
from django.views import generic
from .models import Product

# Create your views here.

class ProductList(generic.ListView):
    queryset = Product.objects.all()
    template_name = "product_list.html"