from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

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
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
