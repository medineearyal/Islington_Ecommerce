from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm, ResetPasswordKeyForm
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.forms.models import inlineformset_factory

from .constants import UserTypeEnum
from .models import AuthUser
from apps.common.models import AddressModel
from ..common.validators import validate_nepali_mobile
from ..orders.constants import NepalProvinceEnum, BagmatiCities, CountryEnum


class AuthUserCreationForm(UserCreationForm):
    class Meta:
        model = AuthUser
        fields = ("email",)


class AuthUserChangeForm(UserChangeForm):
    class Meta:
        model = AuthUser
        fields = ("email",)


class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields["login"].widget.attrs.update(
            {
                "type": "email",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
                "placeholder": "Email Address"
            }
        )
        self.fields["login"].label = "Email Address"
        self.fields["password"].widget.attrs.update(
            {
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
                "pattern": "(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
                "minlength": 8,
                "title": "Must be more than 8 characters, including number, lowercase letter, uppercase letter",
            }
        )


class UserSignupForm(SignupForm):
    first_name = forms.CharField(max_length=255, label="First Name",
                                 error_messages={"required": "First Name is required"})
    last_name = forms.CharField(max_length=255, label="Last Name", error_messages={"required": "Last Name is required"})
    ph_number = forms.CharField(max_length=255, label="Phone Number",
                                error_messages={"required": "Phone Number is required"},
                                validators=[validate_nepali_mobile])
    profile_picture = forms.ImageField(required=False)

    f_name = forms.CharField(max_length=255, label="First Name", required=False)
    l_name = forms.CharField(max_length=255, label="Last Name", required=False)
    street = forms.CharField(max_length=255, label="Street", required=False)
    city = forms.ChoiceField(choices=[("", "Select a city")] + BagmatiCities.choices, required=False)
    state = forms.ChoiceField(choices=[("", "Select a Province")] + NepalProvinceEnum.choices, required=False)
    country = forms.ChoiceField(choices=[("", "Select a Country")] + CountryEnum.choices, required=False)
    zip_code = forms.CharField(max_length=255, label="Zip Code", required=False)
    shipping_email = forms.EmailField(required=False, label="Email Address")
    shipping_ph_number = forms.CharField(max_length=255, label="Phone Number", required=False)

    user_type = forms.ChoiceField(choices=UserTypeEnum.choices)
    seller_qr_code = forms.FileField(required=False)
    seller_bank_name = forms.CharField(max_length=255, label="Bank Name", required=False)
    seller_bank_account_number = forms.CharField(max_length=255, label="Account Number", required=False)
    seller_bank_branch_name = forms.CharField(max_length=255, label="Branch Name", required=False)
    seller_bank_account_name = forms.CharField(max_length=255, label="Account Holder Name", required=False)

    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "type": "email",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )
        self.fields["shipping_email"].widget.attrs.update(
            {
                "type": "email",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )
        self.fields["email"].label = "Email Address"
        self.fields["password1"].widget.attrs.update(
            {
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
                "pattern": "(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
                "minlength": 8,
                "title": "Must be more than 8 characters, including number, lowercase letter, uppercase letter",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
                "pattern": "(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
                "minlength": 8,
                "title": "Must be more than 8 characters, including number, lowercase letter, uppercase letter",
            }
        )
        self.fields["first_name"].widget.attrs.update(
            {
                "placeholder": "First Name",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )
        self.fields["f_name"].widget.attrs.update(
            {
                "placeholder": "First Name",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )
        self.fields["l_name"].widget.attrs.update(
            {
                "placeholder": "Last Name",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )
        self.fields["last_name"].widget.attrs.update(
            {
                "placeholder": "Last Name",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )
        self.fields["ph_number"].widget.attrs.update(
            {
                "placeholder": "Phone Number",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )
        self.fields["shipping_ph_number"].widget.attrs.update(
            {
                "placeholder": "Phone Number",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )
        self.fields["profile_picture"].widget.attrs.update(
            {
                "class": "file-input file-input-[var(--clr-secondary-500)] border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)] bg-[var(--clr-gray-00)]",
            }
        )
        self.fields["seller_qr_code"].widget.attrs.update(
            {
                "class": "file-input file-input-[var(--clr-secondary-500)] border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)] bg-[var(--clr-gray-00)]",
            }
        )
        self.fields["street"].widget.attrs.update(
            {
                "placeholder": "Street",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )
        self.fields["zip_code"].widget.attrs.update(
            {
                "placeholder": "Zip Code",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )
        self.fields["country"].widget.attrs.update(
            {
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full"
            }
        )
        self.fields["user_type"].widget.attrs.update(
            {
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full"
            }
        )
        self.fields["state"].widget.attrs.update(
            {
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full"
            }
        )
        self.fields["city"].widget.attrs.update(
            {
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full"
            }
        )
        self.fields["seller_bank_name"].widget.attrs.update(
            {
                "placeholder": "Bank Name",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )
        self.fields["seller_bank_account_number"].widget.attrs.update(
            {
                "placeholder": "Bank Account Number",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )
        self.fields["seller_bank_branch_name"].widget.attrs.update(
            {
                "placeholder": "Bank Branch",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )
        self.fields["seller_bank_account_name"].widget.attrs.update(
            {
                "placeholder": "Bank Account Holder Name",
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            }
        )

    def clean(self):
        data = self.cleaned_data

        if not data.get("first_name"):
            self.add_error("first_name", "First Name is required")
        if not data.get("last_name"):
            self.add_error("last_name", "Last Name is required")
        if not data.get("email"):
            self.add_error("email", "Email is required")
        if not data.get("ph_number"):
            self.add_error("ph_number", "Phone Number is required")

        if data.get("user_type"):
            if data.get("user_type") == UserTypeEnum.SELLER:
                if not data.get("seller_qr_code"):
                    self.add_error("seller_qr_code", "Please Enter Seller's QR Code")
                if not data.get("seller_bank_name"):
                    self.add_error("seller_bank_name", "Seller's Bank Name is required")
                if not data.get("seller_bank_account_number"):
                    self.add_error("seller_bank_account_number", "Seller's Bank Account Number is required")
                if not data.get("seller_bank_branch_name"):
                    self.add_error("seller_bank_branch_name", "Bank's Branch Name is required")
                if not data.get("seller_bank_account_name"):
                    self.add_error("seller_bank_account_name", "Account Holder's Name is required")
        return data

    def save(self, request):
        user = super().save(request)
        data = self.cleaned_data
        profile_picture = data.get("profile_picture")
        user.ph_number = data.get("ph_number")
        user_type = data.get("user_type")

        if profile_picture:
            user.profile_picture = profile_picture

        if user_type == UserTypeEnum.SELLER:
            user.user_type = user_type
            user.seller_qr_code = data.get("seller_qr_code")
            user.seller_bank_name = data.get("seller_bank_name")
            user.seller_bank_account_number = data.get("seller_bank_account_number")
            user.seller_bank_branch_name = data.get("seller_bank_branch_name")
            user.seller_bank_account_name = data.get("seller_bank_account_name")

        user.save()

        if data.get("shipping_email") and data.get("shipping_ph_number"):
            AddressModel.objects.create(
                user=user,
                street=data.get("street"),
                country=data.get("country"),
                state=data.get("state"),
                city=data.get("city"),
                zip_code=data.get("zip_code"),
                first_name=data.get("f_name"),
                last_name=data.get("l_name"),
                email=data.get("shipping_email"),
                ph_number=data.get("shipping_ph_number"),
            )
        return user


class UserResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email Address"
        self.fields["email"].widget.attrs.update({
            "placeholder": "Your Email Address",
            "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]"
        })

class UserResetPasswordFromKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "New Password"
        self.fields["password1"].widget.attrs.update({
            "placeholder": "Enter a new password",
            "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]"
        })
        self.fields["password2"].label = "Confirm Password"
        self.fields["password2"].widget.attrs.update({
            "placeholder": "Enter the same password as above",
            "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]"
        })