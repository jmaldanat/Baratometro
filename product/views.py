from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import ProductPrice, Product
from perfil.models import SavedProduct, ProductAlert

# Create your views here.

class ProductList(generic.ListView):
    template_name = "product/newindex.html"
    context_object_name = 'productprice_list'
    
    def get_queryset(self):
        # Get top 10 most saved products
        top_products = (
            SavedProduct.objects.values('product')
            .annotate(save_count=Count('product'))
            .order_by('-save_count')[:10]
        )
        
        # Get product IDs from the query
        product_ids = [item['product'] for item in top_products]
        
        # Get the lowest price entry for each popular product
        if product_ids:
            queryset = []
            for product_id in product_ids:
                # Get the lowest price entry for this product
                price_entry = ProductPrice.objects.filter(
                    product_id=product_id
                ).order_by('price').first()
                
                if price_entry:
                    # Add save count as attribute for template use
                    save_count = next(
                        item['save_count'] for item in top_products 
                        if item['product'] == product_id
                    )
                    price_entry.save_count = save_count
                    queryset.append(price_entry)
            return queryset
        else:
            # Fallback to original behavior if no saved products
            return ProductPrice.objects.order_by('product_id', 'price').distinct('product_id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        productprice_list = []
        
        for entry in self.object_list:
            prices = ProductPrice.objects.filter(product=entry.product)
            entry.price_min = min((p.price for p in prices), default=None)
            entry.price_max = max((p.price_max for p in prices if p.price_max is not None), default=None)
            productprice_list.append(entry)
            
        context['productprice_list'] = productprice_list
        context['is_popular_list'] = True  # Flag to indicate this is the popular products list

        # Añadir can_save_more al contexto
        can_save_more = True
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'perfil'):
            can_save_more = user.perfil.can_save_more_products()
        context['can_save_more'] = can_save_more

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
    has_alert = False
    alert_id = None
    if request.user.is_authenticated:
        is_saved = SavedProduct.objects.filter(user=request.user, product=product).exists()
        can_save_more = request.user.perfil.can_save_more_products()
        if is_saved:
            saved_product = SavedProduct.objects.get(user=request.user, product=product)
            alert = ProductAlert.objects.filter(user=request.user, saved_product=saved_product).first()
            if alert:
                has_alert = True
                alert_id = alert.id

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
            "has_alert": has_alert,
            "alert_id": alert_id,
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

@login_required
def create_product_alert(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        saved_product = SavedProduct.objects.get(user=request.user, product=product)
    except SavedProduct.DoesNotExist:
        messages.error(request, "Debes guardar el producto antes de crear una alerta.")
        return redirect('product_detail', slug=product.slug)

    if request.method == 'POST':
        target_price = request.POST.get('target_price')
        channels = request.POST.get('channels', '')
        message = request.POST.get('message', '')
        alert = ProductAlert.objects.filter(user=request.user, saved_product=saved_product).first()
        if alert:
            alert.target_price = target_price
            alert.channels = channels
            alert.message = message
            alert.save()
            messages.success(request, "Alerta actualizada correctamente.")
        else:
            ProductAlert.objects.create(
                user=request.user,
                product=product,
                saved_product=saved_product,
                target_price=target_price,
                channels=channels,
                message=message
            )
            messages.success(request, "Alerta creada correctamente.")
        return redirect('product_detail', slug=product.slug)

    return render(request, 'product/create_alert.html', {
        'product': product,
        'saved_product': saved_product
    })

@login_required
def delete_product_alert(request, alert_id):
    alert = get_object_or_404(ProductAlert, id=alert_id, user=request.user)
    product_slug = alert.product.slug
    alert.delete()
    messages.success(request, "Alerta eliminada correctamente.")
    return redirect('product_detail', slug=product_slug)