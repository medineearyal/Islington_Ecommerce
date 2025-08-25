from django.contrib import admin

from .models import Blog, BlogCategory


# Register your models here.
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status")


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
