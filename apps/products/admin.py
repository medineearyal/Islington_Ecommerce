from django.contrib import admin

from .models import Category, Product, Tag, ProductImage, Badge, ProductBanner, BestDeals


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    fk_name = "product"

class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductImageInline,)

class BestDealsAdmin(admin.ModelAdmin):
    filter_horizontal = ("products", )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Badge)
admin.site.register(ProductBanner)
admin.site.register(ProductImage)
admin.site.register(Product, ProductAdmin)
admin.site.register(BestDeals, BestDealsAdmin)
