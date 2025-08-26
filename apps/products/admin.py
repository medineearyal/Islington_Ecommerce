from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import redirect
from django.urls import path, reverse

from apps.common.mixins import VerifiedProductMixin
from .models import Category, Product, Tag, ProductImage, Badge, ProductBanner, BestDeals, ProductReview, Attribute, \
    ProductAttributeValue, ProductColors, ProductDescription, WishList

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0
    fk_name = "product"


class ProductAttributeInline(admin.StackedInline):
    model = Attribute
    extra = 0

class ProductDescriptionInline(admin.StackedInline):
    model = ProductDescription
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ("colors", )
    inlines = (ProductImageInline, ProductAttributeInline, ProductDescriptionInline)
    list_display = ["name", "seller", "is_verified", "verify_product_button"]

    def verify_product_button(self, obj):
        if not obj.is_verified:
            return format_html(
                "<a class='btn btn-success' href={}>Verify<a/>",
                reverse("admin:verify-product", args=[obj.pk])
            )
        return ""

    verify_product_button.short_description = "Verify"

    def get_urls(self):
        urls = super(ProductAdmin, self).get_urls()

        custom_urls =  [
            path("<int:product_id>/verify/", self.admin_site.admin_view(self.verify_product), name="verify-product"),
        ]

        return custom_urls + urls

    def verify_product(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        product.is_verified = True
        product.save()
        self.message_user(request, f"Product {product} is successfully verified.")
        return redirect(request.META.get("HTTP_REFERER"))



class BestDealsAdmin(admin.ModelAdmin):
    filter_horizontal = ("products", )
    

class ProductBannerAdmin(VerifiedProductMixin, admin.ModelAdmin):
    pass

class WishListAdmin(VerifiedProductMixin, admin.ModelAdmin):
    product_field_name = "products"
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Badge)
admin.site.register(ProductBanner, ProductBannerAdmin)
admin.site.register(ProductImage)
admin.site.register(Attribute)
admin.site.register(ProductDescription)
admin.site.register(ProductAttributeValue)
admin.site.register(ProductColors)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview)
admin.site.register(BestDeals, BestDealsAdmin)
admin.site.register(WishList, WishListAdmin)
