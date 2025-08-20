from django.core.validators import RegexValidator

validate_nepali_mobile = RegexValidator(
    regex=r'^(?:\+977[- ]?)?(?:98|97|96)\d{8}$',
    message="Enter a valid Nepali mobile number."
)