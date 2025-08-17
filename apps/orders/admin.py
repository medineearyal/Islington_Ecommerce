from django.contrib import admin

from .models import Category, Order


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "stock", "status")


admin.site.register(Order, OrderAdmin)
