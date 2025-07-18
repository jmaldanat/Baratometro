from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import SavedProduct, ProductAlert
from product.models import ProductPrice  # importa el modelo de precios
from django.contrib.auth import logout
from django import forms

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
        # Agrega can_save_more al contexto
        can_save_more = True
        if user.is_authenticated and hasattr(user, 'perfil'):
            can_save_more = user.perfil.can_save_more_products()
        context['can_save_more'] = can_save_more
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

class AccountSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'perfil/account_settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        can_save_more = True
        if user.is_authenticated and hasattr(user, 'perfil'):
            can_save_more = user.perfil.can_save_more_products()
        context['can_save_more'] = can_save_more
        # Add any additional context needed for the account settings page
        return context
    
    def post(self, request, *args, **kwargs):
        # Get the profile data from the form
        nombre = request.POST.get('nombre', '')
        telefono = request.POST.get('telefono', '')
        direccion = request.POST.get('direccion', '')
        
        # Update the user's profile
        perfil = request.user.perfil
        perfil.nombre = nombre
        perfil.telefono = telefono
        perfil.direccion = direccion
        perfil.save()
        
        # Add a success message
        messages.success(request, 'Profile information updated successfully!')
        
        # Redirect back to the settings page
        return redirect('profile_account')

class DeleteAccountConfirmForm(forms.Form):
    deleteConfirm = forms.CharField(required=True)
    
    def clean_deleteConfirm(self):
        confirm = self.cleaned_data.get('deleteConfirm')
        if confirm != 'DELETE':
            raise forms.ValidationError("Please type DELETE to confirm account deletion")
        return confirm

class DeleteAccountView(LoginRequiredMixin, FormView):
    form_class = DeleteAccountConfirmForm
    success_url = reverse_lazy('home')  # Redirect to home page after deletion
    
    def form_valid(self, form):
        user = self.request.user
        # Delete the user
        user.delete()
        # Log the user out
        logout(self.request)
        messages.success(self.request, "Your account has been permanently deleted.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "Account deletion failed. Please try again.")
        return redirect('profile_account')

class AlertsView(LoginRequiredMixin, TemplateView):
    template_name = 'perfil/alerts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Obtén todas las alertas de productos del usuario
        product_alerts = ProductAlert.objects.select_related('product').filter(user=user)
        context['product_alerts'] = product_alerts
        return context