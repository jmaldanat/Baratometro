from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product

class Plan(models.Model):
    name = models.CharField(max_length=100)
    product_limit = models.IntegerField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField()

class Perfil(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='perfil')
    nombre = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, related_name='perfiles', null=True, blank=True)

    def __str__(self):
        return self.nombre or str(self.user)

class SavedProduct(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='saved_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='saved_by_users')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_saved_product_per_user')
        ]

    def __str__(self):
        return f"{self.user} saved"

class AlertChannel(models.TextChoices):
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    WHATSAPP = 'whatsapp', 'WhatsApp'
    TELEGRAM = 'telegram', 'Telegram'

class ProductAlert(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='product_alerts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='alerts')
    channels = models.CharField(max_length=100)  # Almacena los canales seleccionados como texto separado por comas
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    message = models.CharField(max_length=255, blank=True)

    def get_channels_list(self):
        return [c for c in self.channels.split(',') if c]

    def __str__(self):
        return f"Alert for {self.product.name} to {self.user} via {self.channels}"
