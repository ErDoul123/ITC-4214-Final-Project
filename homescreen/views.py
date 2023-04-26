from django.shortcuts import render

from products.models import Product, Category


# Create your views here.

def home(request):
    categories = Category.objects.all()
    return render(request, 'homescreen/home.html', {'categories': categories})


def carousel(request):
    recommended_products = Product.objects.filter(is_featured=True)[:5]
    categories = Category.objects.all()
    context = {
        'recommended_products': recommended_products,
        'categories': categories
    }
    return render(request, 'homescreen/home.html', context)
