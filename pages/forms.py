from django import forms


class ContactForm(forms.Form):
    from_name = forms.CharField(
        required=True,
        label="Name",
        widget=forms.EmailInput(attrs={"placeholder": "What's your name?"}),
    )
    from_email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email address"}
        ),
    )
    subject = forms.CharField(
        max_length=60,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Email subject / title"}),
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "What can we help you with?",
                "rows": 10,
                "cols": 5,
            }
        ),
    )
