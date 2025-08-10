from allauth.account.forms import LoginForm, SignupForm
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import AuthUser


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
    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
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
