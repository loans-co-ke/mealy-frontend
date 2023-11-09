from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Admin, Customer

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        if getattr(instance, 'is_admin', False):
            Admin.objects.create(user=instance)
        elif getattr(instance, 'is_customer', False):
            Customer.objects.create(user=instance)