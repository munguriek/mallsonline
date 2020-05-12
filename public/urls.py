from django.urls import path
from .views import *
from django.conf.urls import url
from . import views

urlpatterns = [
path('acades/', views.home_acades, name='home-acades'),
path('shops/', views.home_shops, name='home-shops'),
path('products/', views.home_products, name='home-products'),
path('rooms/<int:id>', views.arcade_rooms, name='home-rooms'),
path('shops/<int:id>', views.arcade_shops, name='arcade-shops'),
path('arcade/<int:id>', views.arcade, name='arcade'),
path('home_shop/<int:id>', views.shop, name='home-shop'),
path('product/<int:id>', views.product, name='product'),
]