from babel.numbers import format_decimal
from django import template

register = template.Library()

@register.filter
def nepali_currency(value):
    try:
        formatted_number = format_decimal(value, format="#,##,##0.00", locale="ne_NP")
        return f"Rs. {formatted_number}"
    except Exception:
        return value