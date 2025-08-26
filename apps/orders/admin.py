from apps.orders.models import Order, Transaction, KhaltiTransaction, OrderStatusLog
from django.contrib import admin

admin.site.register(Order)
admin.site.register(OrderStatusLog)
admin.site.register(Transaction)
admin.site.register(KhaltiTransaction)
