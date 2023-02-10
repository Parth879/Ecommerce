from django.shortcuts import render
from store.models import Product, ProductReview

def index(request):
    products = Product.objects.all().filter(is_available=True).order_by('-created_date')

    reviews = ProductReview.objects.filter(product_id=products)

    context = {
        'products':products,'reviews':reviews
    }   
    return render(request, 'index.html',context)