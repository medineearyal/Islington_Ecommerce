from apps.orders.models import Order, Transaction, KhaltiTransaction, OrderStatusLog
from django.contrib import admin

class OrderAdmin(admin.ModelAdmin):
    list_display = ["uuid", "status"]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ["uuid", "order", "is_payment_success", "payment_method"]

    def payment_method(self, obj):
        return obj.order.payment_option.upper()

    payment_method.short_description = "Payment method"

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStatusLog)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(KhaltiTransaction)
