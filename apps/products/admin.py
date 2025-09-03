from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import path, reverse

from apps.common.mixins import VerifiedProductMixin
from .models import Category, Product, Tag, ProductImage, Badge, ProductBanner, BestDeals, ProductReview, Attribute, \
    ProductAttributeValue, ProductColors, ProductDescription, WishList
from ..common.admin import admin_site


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0
    fk_name = "product"


class ProductAttributeInline(admin.StackedInline):
    model = ProductAttributeValue
    extra = 0

class ProductDescriptionInline(admin.StackedInline):
    model = ProductDescription
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ("colors", )
    inlines = (ProductImageInline, ProductAttributeInline, ProductDescriptionInline)
    list_display = ["name", "seller", "is_verified", "product_action_button"]
    actions = ["verify_products", "reject_products"]

    def verify_products(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} students verified.")

    def reject_products(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"{updated} students rejected.")

    verify_products.short_description = "Verify selected products"
    reject_products.short_description = "Reject selected products"

    def product_action_button(self, obj):
        if not obj.is_verified:
            return format_html(
                "<a class='btn btn-success' href={}>Verify<a/>",
                reverse("admin:toggle-verification", args=[obj.pk])
            )
        else:
            return format_html(
                "<a class='btn btn-danger' href={}>Reject<a/>",
                reverse("admin:toggle-verification", args=[obj.pk])
            )
    product_action_button.short_description = "Action"

    def get_urls(self):
        urls = super(ProductAdmin, self).get_urls()

        custom_urls =  [
            path("<int:product_id>/toggle-verify/", self.admin_site.admin_view(self.toggle_verification), name="toggle-verification"),
        ]

        return custom_urls + urls

    def toggle_verification(self, request, product_id):
        product = Product.objects.get(pk=product_id)

        if product.is_verified:
            product.is_verified = False
            self.message_user(request, f"Product {product} is successfully rejected.", level=messages.SUCCESS)

        else:
            product.is_verified = True
            self.message_user(request, f"Product {product} is successfully verified.", level=messages.SUCCESS)

        product.save()

        return redirect(request.META.get("HTTP_REFERER"))


class BestDealsAdmin(admin.ModelAdmin):
    filter_horizontal = ("products", )
    

class ProductBannerAdmin(VerifiedProductMixin, admin.ModelAdmin):
    pass

class WishListAdmin(VerifiedProductMixin, admin.ModelAdmin):
    product_field_name = "products"
    pass

admin_site.register(Category, CategoryAdmin)
admin_site.register(Tag)
admin_site.register(Badge)
admin_site.register(ProductBanner, ProductBannerAdmin)
admin_site.register(ProductImage)
admin_site.register(Attribute)
admin_site.register(ProductDescription)
admin_site.register(ProductAttributeValue)
admin_site.register(ProductColors)
admin_site.register(Product, ProductAdmin)
admin_site.register(ProductReview)
admin_site.register(BestDeals, BestDealsAdmin)
admin_site.register(WishList, WishListAdmin)
