from django.contrib import admin

from .models import Account, Address


class AddressAdminInline(admin.StackedInline):
    model = Address
    list_display = (
        "street_address_1",
        "street_address_2",
        "town_or_city",
        "county",
        "postcode",
        "country",
        "phone_number",
    )


class AccountAdmin(admin.ModelAdmin):
    inlines = (AddressAdminInline,)

    list_display = (
        "email",
        "first_name",
        "last_name",
        "date_joined",
        "last_login",
        "is_admin",
        "is_staff",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    readonly_fields = ("date_joined", "last_login")

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
