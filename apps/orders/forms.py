from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.widgets import TextInput, EmailInput, Select, CheckboxInput, RadioSelect, Textarea
from .models import Order

class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ("customer", "status",)
        widgets = {
            "first_name": TextInput(attrs={
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full important",
                "placeholder": "First Name"
            }),
            "last_name": TextInput(attrs={
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full important",
                "placeholder": "Last Name"
            }),
            "shipping_street": TextInput(attrs={
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full",
                "placeholder": "Street/Tole"
            }),
            "shipping_country": Select(attrs={
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full",
                "placeholder": "Country"
            }),
            "shipping_region": Select(attrs={
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full",
                "placeholder": "Province/State"
            }),
            "shipping_city": Select(attrs={
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full",
                "placeholder": "City"
            }),
            "shipping_zip_code": TextInput(attrs={
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full",
                "placeholder": "Zip Code"
            }),
            "email": EmailInput(attrs={
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full",
                "placeholder": "Email"
            }),
            "ph_number": TextInput(attrs={
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full",
                "placeholder": "Phone Number"
            }),
            "use_billing_address": CheckboxInput(attrs={
                "class": "w-[20px] h-[20px]"
            }),
            "payment_option": RadioSelect(attrs={
                "class": "radio w-10 h-10 text-[var(--tw-before-bg)] p-1.5 checked:border-3 checked:border-[var(--clr-primary-500)] checked:bg-transparent before:bg-[var(--tw-before-bg)]"
            }),
            "note": Textarea(attrs={
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs text-[var(--clr-gray-900)] px-4 py-3 w-full",
                "placeholder": "Notes about your order, e.g. special notes for delivery"
            })
        }

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        use_billing_address = cleaned_data.get("use_billing_address")

        if use_billing_address:
            if not cleaned_data.get("shipping_street"):
                self.add_error("shipping_street", "Address is required.")
            if not cleaned_data.get("shipping_country"):
                self.add_error("shipping_country", "Country is required.")
            if not cleaned_data.get("shipping_region"):
                self.add_error("shipping_region", "Region is required.")
            if not cleaned_data.get("shipping_city"):
                self.add_error("shipping_city", "City is required.")
            if not cleaned_data.get("shipping_zip_code"):
                self.add_error("shipping_zip_code", "Zip Code is required.")
        return cleaned_data


