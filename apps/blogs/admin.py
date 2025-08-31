from django.contrib import admin

from .models import Blog, BlogCategory
from ..common.admin import admin_site


# Register your models here.
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status")


admin_site.register(Blog, BlogAdmin)
admin_site.register(BlogCategory, BlogCategoryAdmin)
