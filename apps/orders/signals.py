from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver, Signal
from django.template.loader import render_to_string
from .constants import OrderStatusDescription, OrderStatusEnum
from .models import Order, OrderStatusLog, Transaction, SellerPayment
from apps.common.middlewares import get_current_user
from ..common.utils import send_async_email, calculate_redeem_points
from ..users.models import UserRedeemProfile
from django.db.models import F, Sum


@receiver(pre_save, sender=Order)
def create_order_status_log(sender, instance, **kwargs):
    if not instance.pk:
        return

    # old_status = Order.objects.get(pk=instance.pk).status
    # if old_status != instance.status:
    #     OrderStatusLog.objects.create(
    #         order=instance,
    #         status=instance.status,
    #         updated_by=get_current_user(),
    #         note=f"Status changed from {old_status} to {instance.status}"
    #     )
    #     order = instance
    #     html_content = render_to_string("partials/email/order_status.html", {"order": instance, "date": timezone.now().date()})
    #     recipients = [order.email]
    #     send_async_email(recipients, html_content, subject=next(value for key, value in OrderStatusDescription.choices if key == order.status))
    #
    #     if order.status == OrderStatusEnum.DELIVERED:
    #         transaction = get_object_or_404(Transaction, order=instance)
    #         transaction.is_payment_success = True
    #         transaction.save()

payment_successful = Signal()

@receiver(payment_successful)
def send_invoice_on_payment(sender, recipient_list, **kwargs):
    order = kwargs.get("order")
    html_content = render_to_string("partials/email/invoice.html", {"order": order, "total_amount": order.total_amount - order.tax_amount, "date": timezone.now().date()})

    send_async_email(recipient_list, html_content)


# @receiver(pre_save, sender=Transaction)
# def set_redeem_points(sender, instance, **kwargs):
#     if instance.is_payment_success:
#         customer_redeem_points, _ = UserRedeemProfile.objects.get_or_create(user=instance.order.customer)
#         redeem_points = calculate_redeem_points(instance.order.total_amount)
#         UserRedeemProfile.objects.filter(pk=customer_redeem_points.pk).update(
#             orders_completed=F("orders_completed") + 1,
#             redeem_points=F("redeem_points") + redeem_points,
#         )

@receiver(post_save, sender=SellerPayment)
def check_for_transaction_completeness(sender, instance, created, **kwargs):
    if created:
        transaction = get_object_or_404(Transaction, pk=instance.transaction.pk)
        other_payments = SellerPayment.objects.filter(transaction=transaction).exclude(pk=instance.pk)

        previous_sum = 0
        if other_payments.exists():
            previous_sum = other_payments.aggregate(Sum("product_price"))["product_price__sum"]

        if previous_sum + instance.product_price == transaction.order.total_amount - transaction.order.tax_amount:
            transaction.is_payment_success = True
            transaction.remarks = instance.remarks
            transaction.save()

            if transaction.order.status != OrderStatusEnum.DELIVERED:
                transaction.order.status = OrderStatusEnum.DELIVERED
                transaction.order.save()