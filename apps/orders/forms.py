from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, IntegerField, HiddenInput, CharField
from django.forms.fields import DecimalField
from django.forms.widgets import TextInput, EmailInput, Select, CheckboxInput, RadioSelect, Textarea
from .models import Order, OrderCancellation, SellerPayment
from ..common.validators import validate_names


class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ("customer", "status", "total_amount", "tax_amount", "redeemed_amount", "multiple_sellers")
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
                "placeholder": "Email",
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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["email"].required = False
        self.fields["ph_number"].required = False
        self.fields["first_name"].required = False
        self.fields["last_name"].required = False

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        use_billing_address = cleaned_data.get("use_billing_address")

        if not use_billing_address:
            if not cleaned_data.get("first_name"):
                self.add_error("first_name", "First Name is required")
            if not cleaned_data.get("last_name"):
                self.add_error("last_name", "Last Name is required")
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
            if not cleaned_data.get("email"):
                self.add_error("email", "Shipping Email is required")
            if not cleaned_data.get("ph_number"):
                self.add_error("ph_number", "Shipping Phone Number is required")
        else:
            if not getattr(self.user, "billing_address", None):
                self.add_error("use_billing_address", "You Don't Have A Billing Address Set Up. Please Fill Out Before you can use it.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.cleaned_data.get("use_billing_address"):
            billing = self.user.billing_address
            if billing:
                instance.first_name = billing.first_name
                instance.last_name = billing.last_name
                instance.email = billing.email
                instance.ph_number = billing.ph_number
                instance.shipping_street = billing.street
                instance.shipping_country = billing.country
                instance.shipping_state = billing.state
                instance.shipping_city = billing.city
                instance.shipping_zip_code = billing.zip_code

        if commit:
            instance.save()

        return instance



class UserShopOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ["status"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = self.instance
        self.fields["status"].widget.attrs.update({
            "class": f"border rounded-xs border-[{instance.status_with_colors['color']}] w-full text-base p-2 text-[{instance.status_with_colors['color']}]",
            "onchange": "this.form.submit()",
        })


class OrderCancellationForm(ModelForm):
    class Meta:
        model = OrderCancellation
        fields = ["order", "reason"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["order"].widget = HiddenInput()
        self.fields["reason"].label = "Reason for Cancellation"
        self.fields["reason"].widget.attrs.update({
            "class":"border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]",
            "rows": 4
        })



class SellerPaymentForm(ModelForm):
    class Meta:
        model = SellerPayment
        exclude = ["total_amount"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ["remarks", "commission"]:
               field.widget.attrs.update({
                   "readonly": "readonly",
               })
            if name in ["seller", "transaction"]:
                field.widget.attrs.update({
                    "style": "pointer-events: none;"
                })
            if name == "remarks":
                field.widget.attrs.update({
                    "rows": "4"
                })
            field.widget.attrs.update({
                "class": "form-control"
            })

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.total_amount = self.cleaned_data["product_price"] - (self.cleaned_data["product_price"] * self.cleaned_data["commission"]/100)

        if commit:
            instance.save()
        return instance
