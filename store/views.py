from django.shortcuts import render
from products.models import Product


def home(request):
    return render(request, 'store/index.html')


def shop(request):
    # products = Product.objects.all()
    context = {
        'products': [
            {
                "pk": 1,
                "title": "St Saviours OBA Hoodie",
                "slug": "st-saviours-oba-hoodie",
                "description": "St Saviours Hoodie in Club colors.",
                "price": "50.00",
            },
            {
                "pk": 2,
                "title": "St Saviours OBA Tshirt",
                "slug": "st-saviours-oba-tshirt",
                "description": "St Saviours Tshirt in Club Colors",
                "price": "15.00",
            },
            {
                "pk": 3,
                "title": "St Saviours OBA Sweatpants",
                "slug": "st-saviours-oba-sweatpants",
                "description": "St Saviours Sweatpants in Club Colors",
                "price": "40.00",
            }
        ]
    }
    return render(request, 'store/shop.html', context) 
