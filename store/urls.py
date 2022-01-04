from django.urls import path
from .views import home, shop

urlpatterns = [
    path('', home, name='store-home'),
    path('shop/', shop, name='shop')
]
