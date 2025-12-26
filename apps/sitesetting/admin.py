from django.contrib import admin

from .models import SiteSetting
from ..common.admin import admin_site


# Register your models here.
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = (
        "site_title",
        "meta_description",
        "meta_keywords",
        "logo",
        "favicon",
    )


admin_site.register(SiteSetting, SiteSettingAdmin)
