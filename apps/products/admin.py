from django.contrib import admin

from .models import Category, Product, Tag, ProductImage, Badge, ProductBanner, BestDeals, ProductReview, Attribute, \
    ProductAttributeValue, ProductColors, ProductDescription


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1
    fk_name = "product"


class ProductAttributeInline(admin.StackedInline):
    model = Attribute
    extra = 1

class ProductDescriptionInline(admin.StackedInline):
    model = ProductDescription
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ("colors", )
    inlines = (ProductImageInline, ProductAttributeInline, ProductDescriptionInline)

class BestDealsAdmin(admin.ModelAdmin):
    filter_horizontal = ("products", )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
admin.site.register(Badge)
admin.site.register(ProductBanner)
admin.site.register(ProductImage)
admin.site.register(Attribute)
admin.site.register(ProductDescription)
admin.site.register(ProductAttributeValue)
admin.site.register(ProductColors)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview)
admin.site.register(BestDeals, BestDealsAdmin)
