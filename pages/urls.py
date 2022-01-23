from django.urls import path

from .views import (
                    view_about,
                    view_faqs,
                    contact,
                    contact_success,
)

urlpatterns = [
    path('about/', view_about, name='view_about'),
    path('faqs/', view_faqs, name='view_faqs'),
    path("contact/", contact, name="contact"),
    path("contact_success/", contact_success, name="contact_success"),
]
