from django.shortcuts import render
from .models import FAQ
from .forms import ContactForm


def contact(request):
    """
    View to send messages to the site's admins
    """
    context = {}
    if request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            from_email = form.cleaned_data["from_email"]
            message = form.cleaned_data["message"]
            from_name = form.cleaned_data["from_name"]
            mail_msg = f"Message from:\
                 {from_name}\n\n{message}\n\n\
                     Return email address: {from_email}"
            try:
                send_mail(subject, mail_msg, from_email, ["cjcon90@pm.me"])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            messages.success(
                request,
                "Message successfully sent!\nThanks for getting in touch 🙂",
            )
            return redirect("contact_success")
        else:
            context["contact_form"] = form
    else:
        if request.user.is_authenticated:
            form = ContactForm(
                initial={
                    "from_email": request.user.email,
                    "from_name": f"{request.user.first_name}\
                         {request.user.last_name}",
                }
            )
        else:
            form = ContactForm()
    context["contact_form"] = form
    return render(request, "accounts/contact.html", context)


def contact_success(request):
    """
    Confirmation of successful message sent to site admins
    """
    return render(request, "accounts/contact_success.html")

def view_faqs(request):
    """
    Returns frequently asked questions page
    """
    questions = FAQ.objects.all()

    context = {
        'questions': questions,
    }
    return render(request, 'faqs.html', context)
