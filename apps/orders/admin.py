from apps.common.admin import admin_site
from apps.orders.models import Order, Transaction, KhaltiTransaction, OrderStatusLog, SellerPayment, OrderCancellation
from django.contrib import admin

class OrderAdmin(admin.ModelAdmin):
    list_display = ["uuid", "status"]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ["uuid", "order", "is_payment_success", "payment_method"]
    readonly_fields = ["order", "is_payment_success", "remarks"]

    def payment_method(self, obj):
        return obj.order.payment_option.upper()

    payment_method.short_description = "Payment method"

admin_site.register(Order, OrderAdmin)
admin_site.register(OrderStatusLog)
admin_site.register(Transaction, TransactionAdmin)
admin_site.register(KhaltiTransaction)
admin_site.register(SellerPayment)
admin_site.register(OrderCancellation)