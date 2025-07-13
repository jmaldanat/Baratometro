from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import SavedProduct, ProductAlert
from product.models import ProductPrice  # importa el modelo de precios

class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'perfil/perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        saved_products = SavedProduct.objects.select_related('product').filter(user=user)
        # Añade el precio mínimo actual a cada producto guardado
        for saved in saved_products:
            # Obtiene el precio más bajo entre todas las tiendas para el producto guardado
            min_price = (
                ProductPrice.objects
                .filter(product=saved.product)
                .order_by('price')
                .values_list('price', flat=True)
                .first()
            )
            saved.min_price = min_price
        context['saved_products'] = saved_products
        context['product_alerts'] = ProductAlert.objects.select_related('product').filter(user=user)
        return context
        
    def post(self, request, *args, **kwargs):
        """Handle POST requests for deleting saved products"""
        if 'product_id' in request.POST:
            product_id = request.POST.get('product_id')
            try:
                # Get the saved product and verify it belongs to the current user
                saved_product = SavedProduct.objects.get(id=product_id, user=request.user)
                # Delete the saved product
                product_name = saved_product.product.name
                saved_product.delete()
                messages.success(request, f"'{product_name}' has been removed from your saved products.")
            except SavedProduct.DoesNotExist:
                messages.error(request, "Product not found or you don't have permission to delete it.")
        
        # Redirect back to the profile page
        return HttpResponseRedirect(reverse('perfil'))