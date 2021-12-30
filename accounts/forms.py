from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)
    newsletter = forms.TypedChoiceField(
        coerce=lambda x: x == "True",
        choices=(
            (True, "Yes"),
            (False, "No"),
        ),
        widget=forms.RadioSelect,
        initial=True,
    )

    class Meta:
        model = Account
        fields = (
            "email",
            "first_name",
            "last_name",
            "newsletter",
            "password1",
            "password2",
        )
