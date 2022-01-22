from django.urls import path

from .views import (
                    view_faqs,
                    contact,
                    contact_success
)

urlpatterns = [
    path("contact/", contact, name="contact"),
    path("contact_success/", contact_success, name="contact_success"),
    path('faqs', view_faqs, name='view_faqs'),
]