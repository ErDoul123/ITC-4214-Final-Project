from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('products', views.products_view, name="products"),
    path('search', views.search_view, name='search'),
    path('add-product', views.add_product, name='add-product'),
    path('product-details/<int:id>/', views.product_details, name='product-details'),
    path('update-product/<int:pk>/', views.update_product, name='update_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('categories/', views.category_list, name='category_list'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category_products/<int:category_id>/', views.category_products, name='category_products'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
