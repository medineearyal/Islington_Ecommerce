from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver, Signal
from django.template.loader import render_to_string
from .constants import OrderStatusDescription, OrderStatusEnum
from .models import Order, OrderStatusLog, Transaction
from apps.common.middlewares import get_current_user
from ..common.utils import send_async_email, calculate_redeem_points
from ..users.models import UserRedeemProfile
from django.db.models import F

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
        order = instance
        html_content = render_to_string("partials/email/order_status.html", {"order": instance, "date": timezone.now().date()})
        recipients = [order.email]
        send_async_email(recipients, html_content, subject=next(value for key, value in OrderStatusDescription.choices if key == order.status))

        if order.status == OrderStatusEnum.DELIVERED:
            transaction = get_object_or_404(Transaction, order=instance)
            transaction.is_payment_success = True
            transaction.save()

payment_successful = Signal()

@receiver(payment_successful)
def send_invoice_on_payment(sender, recipient_list, **kwargs):
    order = kwargs.get("order")
    html_content = render_to_string("partials/email/invoice.html", {"order": order, "total_amount": order.total_amount - order.tax_amount, "date": timezone.now().date()})

    send_async_email(recipient_list, html_content)


@receiver(pre_save, sender=Transaction)
def set_redeem_points(sender, instance, **kwargs):
    if instance.is_payment_success:
        customer_redeem_points, _ = UserRedeemProfile.objects.get_or_create(user=instance.order.customer)
        redeem_points = calculate_redeem_points(instance.order.total_amount)
        UserRedeemProfile.objects.filter(pk=customer_redeem_points.pk).update(
            orders_completed=F("orders_completed") + 1,
            redeem_points=F("redeem_points") + redeem_points,
        )