from django.contrib import admin
from .models import Product, Store, ProductPrice, ProductPriceStatus, PriceHistory

# Register your models here.
admin.site.register(Product)
admin.site.register(Store)
admin.site.register(ProductPrice)
admin.site.register(ProductPriceStatus)
admin.site.register(PriceHistory)