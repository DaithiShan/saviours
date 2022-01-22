from django.contrib import admin
from .models import FAQ


# ------ FAQs ------


class FAQAdmin(admin.ModelAdmin):
    """
    Create admin views for frequently asked questions
    """
    list_display = (
        'question',
        'answer',
    )


# Register Swim Programe and FAQs models
admin.site.register(FAQ, FAQAdmin)