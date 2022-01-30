from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Form collects shipping information on order
    """

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-genetate
        labels and set autofocus on first field
        """
        # call default init to set form up
        super().__init__(*args, **kwargs)

        # dictionary for form fields
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Eircode',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
            'country': 'Country'
        }

        # cursor will start in full name field
        self.fields['first_name'].widget.attrs['autofocus'] = True

        # iterate through form fields
        for field in self.fields:
            # remove 'country' placeholder
            if field != 'country':
                # Add * to placeholder, if required
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]

                # setting placeholder attributes to dictionary values
                self.fields[field].widget.attrs['placeholder'] = placeholder

            # add CSS class
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'

            # remove form field labels
            self.fields[field].label = False
