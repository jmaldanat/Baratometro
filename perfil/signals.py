from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Perfil, Plan

@receiver(post_save, sender=get_user_model())
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        # Get the free plan specifically
        plan_default = Plan.objects.filter(name="free").first()
        # Create the profile and copy the email from the user account
        Perfil.objects.create(
            user=instance, 
            plan=plan_default,
            email=instance.email  # Copy email from user to perfil
        )