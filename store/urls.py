from django.urls import path
from .views import home, shop, search

urlpatterns = [
    path('', home, name='store-home'),
    path('shop/', shop, name='shop'),
    path('shop/<slug:category>/', shop, name='shop'),
    path('shop/<slug:category>/<slug:subcategory>/', shop, name='shop'),
    path('search', search, name='search'),
]
