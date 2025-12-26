from allauth.account.models import EmailAddress
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group
from django.utils.html import format_html

from apps.common.admin import admin_site
from apps.users.models import AuthUser, UserRedeemProfile
from django.urls import reverse, path
from django.shortcuts import redirect
from apps.common.models import AddressModel

# Register your models here.
User = get_user_model()

class AddressModelInlineAdmin(admin.StackedInline):
    model = AddressModel
    extra = 0
    min_num = 1
    max_num = 1
    validate_max = True
    validate_min = True
    can_delete = False
    verbose_name = "User's Billing Address"

class AuthUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = AuthUser
    list_display = ("email", "user_type", "is_verified_seller", "is_staff", "is_active", "verify_seller_btn")
    list_filter = ("email", "is_staff", "is_active")
    inlines = [AddressModelInlineAdmin, ]
    fieldsets = (
        (
            "Personal Details",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password",
                    "profile_picture",
                    "ph_number",
                    "user_type",
                    "is_verified_seller"
                )
            },
        ),
        (
            "Seller Details",
            {
                "fields": (
                    "seller_shop_logo",
                    "seller_qr_code",
                    "seller_bank_name",
                    "seller_bank_account_number",
                    "seller_bank_branch_name",
                    "seller_bank_account_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_staff", "is_active", "groups", "user_permissions"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        staff_group = Group.objects.get(name="Staffs")

        if form.instance.is_staff and not form.instance.is_superuser and not staff_group in form.instance.groups.all():
            form.instance.groups.add(staff_group)

    def verify_seller_btn(self, obj):
        if not obj.is_staff and not obj.is_superuser and not obj.is_verified_seller:
            return format_html(
                '<a class="btn btn-success btn-sm" href="{}">Verify</a>',
                reverse("admin:verify-seller", args=[obj.pk])
            )
        return ""

    verify_seller_btn.short_description = "Verify Seller"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<int:seller_id>/verify/", self.admin_site.admin_view(self.verify_seller), name="verify-seller"),
        ]
        return custom_urls + urls

    def verify_seller(self, request, seller_id, *args, **kwargs):
        seller = User.objects.get(pk=seller_id)
        seller.is_verified_seller = True
        seller.save()
        self.message_user(request, f"Seller {seller} is successfully verified.")
        return redirect(request.META.get("HTTP_REFERER"))

admin_site.register(AuthUser, AuthUserAdmin)
admin_site.register(UserRedeemProfile)
admin_site.register(EmailAddress)