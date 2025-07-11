from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    ean = models.CharField(max_length=50, unique=True)  # Código EAN/barcode
    category = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Genera slug automático a partir del nombre
            base_slug = slugify(self.name)
            
            # Si el producto es nuevo (no tiene ID), guarda primero sin slug
            if not self.pk:
                self.slug = base_slug
                super(Product, self).save(*args, **kwargs)
            
            # Ahora que tenemos el ID, actualiza el slug con el ID
            self.slug = f"{base_slug}-{self.pk}"
        
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=255)
    logo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name   


class ProductPriceStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name    

class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(ProductPriceStatus, on_delete=models.SET_NULL, null=True, related_name='product_prices_status')
    updated_on = models.DateTimeField(auto_now=True)
    price_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_on = models.DateField(null=True, blank=True)
    max_on = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to update historical min/max prices.
        """
        today = date.today()

        # Initialize min/max prices if they are not set (for new or migrated objects)
        if self.price_min is None:
            self.price_min = self.price
            self.min_on = today
        
        if self.price_max is None:
            self.price_max = self.price
            self.max_on = today

        # Update min price if current price is lower
        if self.price < self.price_min:
            self.price_min = self.price
            self.min_on = today

        # Update max price if current price is higher
        if self.price > self.price_max:
            self.price_max = self.price
            self.max_on = today
            
        super(ProductPrice, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} at {self.store.name} - ${self.price}"

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} at {self.store.name} on {self.checked_at} - ${self.price}"