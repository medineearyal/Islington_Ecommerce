from django import forms

from apps.common.models import AddressModel


class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressModel
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "border rounded-xs border-[var(--clr-gray-100)] w-full text-base p-2 text-[var(--clr-gray-900)]"
            })
