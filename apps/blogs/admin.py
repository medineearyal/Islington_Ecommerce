from django.contrib import admin

from .models import Blog


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status")


admin.site.register(Blog, BlogAdmin)
