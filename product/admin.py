from django.contrib import admin
from django.db.models import Count
from .models import Product, Store, ProductPrice, ProductPriceStatus, PriceHistory
from django_summernote.admin import SummernoteModelAdmin

@admin.register(ProductPrice)
class ProductPriceAdmin(SummernoteModelAdmin):
    """
    Admin configuration for the ProductPrice model using SummernoteModelAdmin.

    - Utiliza el decorador @admin.register(ProductPrice) para registrar la clase ProductPriceAdmin directamente en el admin de Django, evitando la necesidad de llamar a admin.site.register manualmente.
    - list_display: Especifica los campos que se mostrarán en la lista de objetos ProductPrice en el panel de administración.
    - search_fields: Permite buscar productos por nombre ('name') o código EAN ('ean') usando la relación con el modelo Product mediante '__'.
    - list_filter: Añade filtros laterales para los campos 'store', 'created_on', 'updated_on' y 'status', facilitando la navegación y gestión de los registros en el admin.
    """
    list_display = ('product', 'price', 'store', 'created_on', 'updated_on', 'status')
    # El uso de '__' permite buscar en campos de modelos relacionados (en este caso, 'name' y 'ean' del modelo Product)
    search_fields = ('product__name', 'product__ean')
    list_filter = ('store', 'created_on', 'updated_on', 'status')

class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Product model.
    """
    list_display = ('name', 'ean', 'category', 'created_on', 'saved_by_count')
    search_fields = ('name', 'ean', 'category')
    list_filter = ('category', 'created_on',)
    readonly_fields = ('saved_by_count',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(saved_count=Count('saved_by_users'))
        return queryset
        
    def saved_by_count(self, obj):
        return obj.saved_count
    saved_by_count.admin_order_field = 'saved_count'
    saved_by_count.short_description = 'Saved by Users'

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Store)
admin.site.register(ProductPriceStatus)
admin.site.register(PriceHistory)