from django.contrib import admin

from .models import SiteSetting


# Register your models here.
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = (
        "site_title",
        "meta_description",
        "meta_keywords",
        "logo",
        "favicon",
    )


admin.site.register(SiteSetting, SiteSettingAdmin)
