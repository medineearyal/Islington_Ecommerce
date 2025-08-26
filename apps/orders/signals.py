from django.db.models.signals import pre_save
from django.dispatch import receiver, Signal
from django.template.loader import render_to_string

from .models import Order, OrderStatusLog
from apps.common.middlewares import get_current_user
from ..common.utils import send_invoice_email_async


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

payment_successful = Signal()

@receiver(payment_successful)
def send_invoice_on_payment(sender, recipient_list, **kwargs):
    order = kwargs.get("order")
    html_content = render_to_string("partials/email/invoice.html", {"order": order, "total_amount": order.total_amount - order.tax_amount})

    send_invoice_email_async(recipient_list, html_content)