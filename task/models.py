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

# Signal to trigger Celery task when a Task instance is created
@receiver(post_save, sender=Task)
def task_post_save(sender, instance, created, **kwargs):
    if created:  # Only when a new Task is created
        from task.tasks import process_task
        # Enqueue the Celery task with both task ID and URL
        process_task.delay(instance.id, instance.url)