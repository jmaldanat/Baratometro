from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver


class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=255)
    content = models.TextField()
    description = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    finished_on = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        perfil = getattr(self.user, 'perfil', None)
        if perfil and not perfil.can_save_more_products():
            # Prevent saving if user cannot save more products
            return
        super().save(*args, **kwargs)

# Signal to trigger Celery task when a Task instance is created
@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    if created:
        from product.models import ProductPrice
        from perfil.models import SavedProduct

        # First, check if user can save more products
        perfil = getattr(instance.user, 'perfil', None)
        if perfil and perfil.can_save_more_products():
            # Then, check if the URL exists in ProductPrice.link
            price_entry = ProductPrice.objects.filter(link=instance.url).select_related('product').first()
            if price_entry:
                # Mark task as completed
                instance.status = 'completed'
                instance.product = price_entry.product
                instance.save(update_fields=['status', 'product'])

                SavedProduct.objects.get_or_create(
                    user=instance.user,
                    product=price_entry.product
                )
            else:
                # Enqueue the Celery task with both task ID and URL
                from task.tasks import process_task
                process_task.delay(instance.id, instance.url)
        else:
            # Optionally, handle the case when user cannot save more products
            pass