from django.contrib import admin

from .models import Page
from ..common.admin import admin_site


# Register your models here.


class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "content")


admin_site.register(Page, PageAdmin)
