from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Plan, Perfil, SavedProduct, ProductAlert

class PlanAdmin(SummernoteModelAdmin):
    list_display = ('name', 'product_limit', 'price_per_month')
    summernote_fields = ('features',)

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre', 'email', 'telefono', 'plan', 'created_at')
    search_fields = ('nombre', 'email', 'user__username')

@admin.register(SavedProduct)
class SavedProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    search_fields = ('user__username', 'product__name')

@admin.register(ProductAlert)
class ProductAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'channels', 'active', 'created_at')
    list_filter = ('active', 'channels')
    search_fields = ('user__username', 'product__name')

admin.site.register(Plan, PlanAdmin)