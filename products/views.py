import os

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.is_authenticated and user.is_superuser


def products_view(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products/products.html', context)


def search_view(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        products = Product.objects.filter(name__icontains=searched)
        context = {'searched': searched, 'products': products}
        return render(request, 'products/search.html', context)
    else:
        message = 'Please enter a product name to search'
        context = {'message': message}
        return render(request, 'products/search.html', context)


@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            image_file = request.FILES.get('image')
            if not image_file:
                form.add_error('image', 'Please upload an image.')
                messages.success(request, "Please Provide an Image for the Product!")
                return render(request, 'products/add_product.html', {'form': form})
            product.image = handle_uploaded_image(image_file)
            product.save()
            messages.success(request, "Product Added Successfully!")
            return redirect('products')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})


def handle_uploaded_image(image_file):
    if not image_file:
        raise ValueError("Image file is required")
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'images'))
    filename = fs.save(image_file.name, image_file)
    return os.path.join(settings.MEDIA_ROOT, 'images', filename)


def product_details(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'products/product_details.html', {'product': product})


@login_required
@user_passes_test(is_admin)
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product-details', id=product.pk)
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/update_product.html', context)


@login_required
@user_passes_test(is_admin)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('products')
    else:
        context = {'product': product}
        return render(request, 'products/delete_product.html', context)


@login_required
@user_passes_test(is_admin)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})


@login_required
@user_passes_test(is_admin)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'confirm_delete_category.html', {'category': category})


@login_required
@user_passes_test(is_admin)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            new_category = Category(name=category_name)
            new_category.save()
            messages.success(request, 'Category has been added.')
            return redirect('category_list')
    else:
        form = CategoryForm()
    context = {'form': form}
    return render(request, 'products/add_category.html', context)


def category_products(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'products/category_products.html', context)
