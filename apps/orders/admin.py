from apps.orders.models import Order, Transaction, KhaltiTransaction
from django.contrib import admin

admin.site.register(Order)
admin.site.register(Transaction)
admin.site.register(KhaltiTransaction)
