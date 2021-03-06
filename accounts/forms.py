from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import Account, Address

# Custom forms adapted from CodingWithMitch:
# https://www.youtube.com/playlist?list=PLgCYzUzKIBE_dil025VAJnDjNZHHHR9mW


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)

    class Meta:
        model = Account
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid email and/or password")


class EditAccountForm(forms.ModelForm):
    email = forms.EmailField(max_length=60)

    class Meta:
        model = Account
        fields = ("first_name", "last_name", "email")


class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        required=True,
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Please confirm your password"}
        ),
    )


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            "street_address_1",
            "street_address_2",
            "town_or_city",
            "county",
            "postcode",
            "country",
            "phone_number",
        )
        labels = {
            "street_address_1": "Address 1",
            "street_address_2": "Address 2 (optional)",
            "town_or_city": "Town / City",
        }
