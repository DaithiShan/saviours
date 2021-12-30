from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from .models import Account
from .forms import RegistrationForm


def register_user(request):
    """
    View to register new users to the website
    """
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        redirect_url = request.POST.get("next") or "home"
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            raw_password = form.cleaned_data.get("password1")
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            # messages.success(
            #     request,
            #     f"Thanks for registering,\
            #         {request.user.first_name}! You are now logged in 🙂",
            # )
            return redirect(redirect_url)
        else:
            context["registration_form"] = form
    else:  # GET request
        form = RegistrationForm()
        context["registration_form"] = form
    return render(request, "accounts/register.html", context)

# Create your views here.
