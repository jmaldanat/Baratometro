from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ProductPrice, Product
from perfil.models import SavedProduct

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
    product_prices = get_list_or_404(
        ProductPrice.objects.select_related('store', 'product').order_by('price'), 
        product__slug=slug
    )
    product = product_prices[0].product if product_prices else None

    prices = [p.price for p in product_prices]
    min_price = min(prices) if prices else None
    max_price = max(prices) if prices else None
    
    # Calculate percentage above minimum price for each product price
    if min_price:
        for price in product_prices:
            if price.price == min_price:
                price.percentage_above_min = 0
            else:
                price.percentage_above_min = int(round(((price.price - min_price) / min_price) * 100))
    
    # Verificar si el usuario ha guardado este producto
    is_saved = False
    can_save_more = True
    if request.user.is_authenticated:
        is_saved = SavedProduct.objects.filter(user=request.user, product=product).exists()
        can_save_more = request.user.perfil.can_save_more_products()

    return render(
        request,
        "product/newproduct_detail.html",
        {
            "product": product,
            "product_prices": product_prices,
            "min_price": min_price,
            "max_price": max_price,
            "is_saved": is_saved,
            "can_save_more": can_save_more,
        },
    )

@login_required
def save_product(request, product_id):
    if request.method == 'POST':
        # Verificar si el usuario puede guardar más productos
        if not request.user.perfil.can_save_more_products():
            messages.error(
                request, 
                f"Has alcanzado el límite de productos guardados para tu plan ({request.user.perfil.plan.name}). "
                f"Actualiza a un plan superior para guardar más productos."
            )
            return redirect('product_detail', slug=request.POST.get('product_slug'))
            
        # Continuar con el proceso de guardar el producto
        product = get_object_or_404(Product, pk=product_id)
        saved_product, created = SavedProduct.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if created:
            messages.success(request, "Producto guardado correctamente.")
        else:
            messages.info(request, "Este producto ya estaba en tu lista.")
            
        return redirect('product_detail', slug=product.slug)
    
    # Si no es POST, redirigir a la página del producto
    return redirect('home')

@login_required
def unsave_product(request, product_id):
    if request.method == 'POST':
        try:
            saved_product = SavedProduct.objects.get(user=request.user, product_id=product_id)
            saved_product.delete()
            messages.success(request, "Producto eliminado de tu lista.")
        except SavedProduct.DoesNotExist:
            messages.error(request, "No se encontró el producto en tu lista.")
        return redirect('product_detail', slug=request.POST.get('product_slug'))
    return redirect('home')