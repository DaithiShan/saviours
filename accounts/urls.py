from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
                    register_user,
                    logout_user,
                    login_user,
                    account_details,
                    edit_account_details,
                    delete_account,
                    add_address,
                    edit_address,
                    my_orders,
)

urlpatterns = [
    path("register/", register_user, name="register"),
    path("logout/", logout_user, name="logout"),
    path("login/", login_user, name="login"),
    path("details/", account_details, name="account_details"),
    path(
        "details/edit/",
        edit_account_details,
        name="edit_account_details",
    ),
    path(
        "details/delete/",
        delete_account,
        name="delete_account",
    ),
    path("address/new/", add_address, name="add_address"),
    path("address/edit/", edit_address, name="edit_address"),
    path("orders/", my_orders, name="my_orders"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
