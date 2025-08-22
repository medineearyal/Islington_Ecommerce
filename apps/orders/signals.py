from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order, OrderStatusLog
from apps.common.middlewares import get_current_user

@receiver(pre_save, sender=Order)
def create_order_status_log(sender, instance, **kwargs):
    if not instance.pk:
        return

    old_status = Order.objects.get(pk=instance.pk).status
    if old_status != instance.status:
        OrderStatusLog.objects.create(
            order=instance,
            status=instance.status,
            updated_by=get_current_user(),
            note=f"Status changed from {old_status} to {instance.status}"
        )