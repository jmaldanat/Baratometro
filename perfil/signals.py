from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Perfil, Plan

@receiver(post_save, sender=get_user_model())
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        # Puedes asignar un plan por defecto si lo deseas
        plan_default = Plan.objects.first()
        Perfil.objects.create(user=instance, plan=plan_default)