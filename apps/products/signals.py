from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Product
from .utils import generate_unique_sku


@receiver(pre_save, sender=Product)
def sku_generation_and_identifier_format(sender, instance, **kwargs):
    if not instance.sku:
        instance.sku = generate_unique_sku(instance.category.name, instance.pk or 0, instance.name)