from django.urls import path
from .views import (checkout,
                    order_review,
                    order_details,
                    order_complete)
from .webhooks import webhook


urlpatterns = [
    path('', checkout, name='checkout'),
    path('review/', order_review, name='order_review'),
    path('details/', order_details, name='order_details'),
    path('complete/<order_number>', order_complete,
         name='order_complete'),
    path('wh/', webhook, name='webhook'),
]
