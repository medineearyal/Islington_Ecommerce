from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from apps.users.models import AuthUser


# Register your models here.
class AuthUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = AuthUser
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("email", "is_staff", "is_active")
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


admin.site.register(AuthUser, AuthUserAdmin)
