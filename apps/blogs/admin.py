from django.contrib import admin

from .models import Blog, Category


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "status")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
