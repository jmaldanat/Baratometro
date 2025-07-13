from django.shortcuts import render,  get_list_or_404, get_object_or_404
from django.views import generic
from .models import ProductPrice

# Create your views here.

class ProductList(generic.ListView):
    queryset = ProductPrice.objects.order_by('product_id', 'price').distinct('product_id')
    template_name = "product/newindex.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productprice_list = []
        for entry in self.queryset:
            prices = ProductPrice.objects.filter(product=entry.product)
            entry.price_min = min((p.price for p in prices), default=None)
            entry.price_max = max((p.price_max for p in prices if p.price_max is not None), default=None)
            productprice_list.append(entry)
        context['productprice_list'] = productprice_list
        return context


def product_detail(request, slug):
    product_prices = get_list_or_404(ProductPrice.objects.select_related('store', 'product'), product__slug=slug)
    product = product_prices[0].product if product_prices else None

    prices = [p.price for p in product_prices]
    min_price = min(prices) if prices else None
    max_price = max(prices) if prices else None

    return render(
        request,
        "product/newproduct_detail.html",
        {
            "product": product,
            "product_prices": product_prices,
            "min_price": min_price,
            "max_price": max_price,
        },
    )