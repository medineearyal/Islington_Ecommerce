from datetime import timedelta, datetime

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth

from apps.common.models import AddressModel, Notices
from apps.common.utils import months_ago
from apps.orders.constants import OrderStatusEnum
from apps.orders.models import Order, Transaction
from apps.users.constants import UserTypeEnum
from django.utils import timezone

# Register your models here.
User = get_user_model()
class MyAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}

        total_orders = Order.objects.count()
        pending_orders = Order.objects.exclude(status__in=[OrderStatusEnum.DELIVERED, OrderStatusEnum.CANCELED]).count()
        completed_orders = Order.objects.filter(status=OrderStatusEnum.DELIVERED).count()
        total_revenue = Transaction.objects.filter(is_payment_success=True).aggregate(Sum("order__total_amount"))["order__total_amount__sum"] or 0
        total_sellers = User.objects.filter(user_type=UserTypeEnum.SELLER).count()

        chart_labels = ["Pending", "Completed", "Canceled"]
        chart_data = [
            Order.objects.exclude(status__in=[OrderStatusEnum.DELIVERED, OrderStatusEnum.CANCELED]).count(),
            Order.objects.filter(status=OrderStatusEnum.DELIVERED).count(),
            Order.objects.filter(status=OrderStatusEnum.CANCELED).count()
        ]

        three_months_ago = months_ago(2)

        orders_last_3_months = (
            Order.objects
            .filter(created__gte=three_months_ago)
            .annotate(month=TruncMonth('created'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )

        last_3_month_labels = [o['month'].strftime("%b") for o in orders_last_3_months]
        last_3_month_orders = [o['count'] for o in orders_last_3_months]

        extra_context.update({
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "completed_orders": completed_orders,
            "total_revenue": total_revenue,
            "total_sellers": total_sellers,
            "chart_labels": chart_labels,
            "chart_data": chart_data,
            'last_3_month_labels': last_3_month_labels,
            'last_3_month_orders': last_3_month_orders
        })

        return super().index(request, extra_context=extra_context)

admin_site = MyAdminSite(name="islington_ecommerce_admin")

admin_site.register(AddressModel)
admin_site.register(Notices)