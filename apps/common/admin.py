from django.contrib import admin

from apps.common.models import AddressModel, Notices

# Register your models here.
admin.site.register(AddressModel)
admin.site.register(Notices)