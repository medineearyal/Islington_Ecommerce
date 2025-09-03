from django import forms
from django.forms import inlineformset_factory

from apps.products.models import ProductReview, Product, ProductImage, ProductDescription, Category, ProductColors, \
    ProductAttributeValue, Attribute


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        exclude = ["review_from", "product"]
        labels = {
            "rating": "Rating",
            "feedback": "Feedback",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rating"].widget = forms.HiddenInput()
        self.fields["feedback"].widget.attrs.update({
            "placeholder": "Write down your feedback about our product & services",
        })
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]"
            })

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating <= 0:
            raise forms.ValidationError("Rating Is Required")
        return rating

    def clean_feedback(self):
        feedback = self.cleaned_data["feedback"]
        if not feedback:
            raise forms.ValidationError("Feedback Is Required")
        return feedback


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["seller", "sku", "is_featured", "is_header_banner", "headline", "tags", "slug", "status", "is_verified"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]"
            })

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ["slug"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].widget.attrs.update({
            "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]"
        })

class ProductColorsForm(forms.ModelForm):
    class Meta:
        model = ProductColors
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]"
            })

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = ["name", "datatype"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]"
            })

class ProductAttributeValueForm(forms.ModelForm):
    class Meta:
        model = ProductAttributeValue
        fields = ["attribute", "value"]
        widgets = {
            "attribute": forms.Select(attrs={
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs px-4 py-3 w-full"
            }),
            "value": forms.TextInput(attrs={
                "class": "ring ring-[var(--clr-gray-100)] rounded-xs px-4 py-3 w-full",
                "placeholder": "Enter value"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["attribute"].required = False
        self.fields["value"].required = False
        self.fields["value"].help_text = "Please Enter the values as Comma Separated Values, for Eg: X, XL, XXL"

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False

class ProductDescriptionForm(forms.ModelForm):
    class Meta:
        model = ProductDescription
        fields = ["title", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].required = False
        self.fields["description"].required = False


ImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=0, can_delete=True)
DescriptionFormSet = inlineformset_factory(Product, ProductDescription, form=ProductDescriptionForm, extra=0, can_delete=True)
AttributeFormset = inlineformset_factory(Product, ProductAttributeValue, form=ProductAttributeValueForm, extra=0, can_delete=True, fk_name="product")
