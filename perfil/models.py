from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product

class Plan(models.Model):
    name = models.CharField(max_length=100)
    product_limit = models.IntegerField()
    price_per_month = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField()

    def __str__(self):
        return self.name

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

    def can_save_more_products(self):
        """Verifica si el usuario puede guardar más productos según su plan"""
        if not self.plan:
            return False

        current_saved_count = SavedProduct.objects.filter(user=self.user).count()
        return current_saved_count < self.plan.product_limit

    def saved_products_count(self):
        """Retorna el número de productos guardados por el usuario"""
        return SavedProduct.objects.filter(user=self.user).count()

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
    saved_product = models.ForeignKey('SavedProduct', on_delete=models.CASCADE, related_name='alerts', null=True)
    channels = models.CharField(max_length=100)  # Almacena los canales seleccionados como texto separado por comas
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    message = models.CharField(max_length=255, blank=True)
    target_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Nuevo campo

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'saved_product'], name='unique_alert_per_saved_product')
        ]

    def get_channels_list(self):
        return [c for c in self.channels.split(',') if c]

    @property
    def min_price_now(self):
        prices = self.product.prices.values_list('price', flat=True)
        return min(prices) if prices else None

    @property
    def store_with_min_price(self):
        min_price_obj = self.product.prices.order_by('price').first()
        return min_price_obj.store if min_price_obj else None

    def __str__(self):
        return f"Alert for {self.product.name} to {self.user} via {self.channels}"
