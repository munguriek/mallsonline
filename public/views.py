from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import  Q, Count
from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	CreateView
	)
from .models import*
from users.models import*
from acade_owner.models import*
from django.db import IntegrityError
from django.db.models import Sum

def home_acades(request):
	acades = Acade.objects.annotate(number_of_rooms=Count('room', filter=Q(room__status=1)), number_of_shops=Count('room__book__shop')).order_by('-number_of_rooms','-number_of_shops')
	context = {
	'title': 'Acades',
	'acades': acades,
	}

	return render(request, 'public/acades.html', context)

def home_shops(request):
	shops = Shop.objects.all().order_by('-id')
	context = {
	'title': 'Shops',
	'shops': shops,
	}

	return render(request, 'public/shops.html', context)

def home_products(request):
	products = Product.objects.all().order_by('-id')
	context = {
	'title': 'Products',
	'products': products,
	}

	return render(request, 'public/products.html', context)

def arcade_rooms(request, id):
	acade=Acade.objects.get(pk=id)
	rooms = Room.objects.filter(acade=acade, status=1).order_by('-id')
	context = {
	'title': acade.name,
	'head': acade.name,
	'rooms': rooms,
	}

	return render(request, 'public/rooms.html', context)

def arcade_shops(request, id):
	acade=Acade.objects.get(pk=id)
	shops = Shop.objects.filter(room__room__acade=acade).order_by('-id')
	context = {
	'title': acade.name,
	'head': acade.name,
	'shops': shops,
	}

	return render(request, 'public/shops.html', context)

def arcade(request, id):
	acade=Acade.objects.get(pk=id)
	shops = Shop.objects.filter(room__room__acade=acade).order_by('-id')
	total_shops = Shop.objects.filter(room__room__acade=acade).count()
	rooms = Room.objects.filter(acade=acade).order_by('-id')
	total_rooms = Room.objects.filter(acade=acade).count()
	free_rooms = Room.objects.filter(acade=acade, status=1).order_by('-id')
	total_free_rooms = Room.objects.filter(acade=acade, status=1).count()
	visitors = Visitor.objects.filter(acade=acade).order_by('-id')
	total_visitors = Visitor.objects.filter(acade=acade).count()
	acades = Acade.objects.annotate(number_of_rooms=Count('room', filter=Q(room__status=1)), number_of_shops=Count('room__book__shop')).order_by('-number_of_rooms','-number_of_shops')
	paginator = Paginator(acades, 3)
	page = request.GET.get('page')
	acades = paginator.get_page(page)
	context = {
	'title': acade.name,
	'head': acade.name,
	'acade': acade,
	'acades': acades,
	'shops': shops,
	'total_shops': total_shops,
	'rooms': rooms,
	'total_rooms': total_rooms,
	'total_free_rooms': total_free_rooms,
	'free_rooms': free_rooms,
	'visitors': visitors,
	'total_visitors': total_visitors,
	}

	return render(request, 'public/arcade.html', context)

def shop(request, id):
	shop=Shop.objects.get(pk=id)
	shops = Shop.objects.filter(room__room__acade=shop.room.room.acade).exclude(id=shop.id).order_by('-id')
	total_shops = Shop.objects.filter(room__room__acade=shop.room.room.acade).count()
	paginator = Paginator(shops, 3)
	page = request.GET.get('page')
	shops = paginator.get_page(page)
	products = Product.objects.filter(shop=shop, status=1).order_by('-id')
	context = {
	'title': shop.name,
	'head': shop.name,
	'shop': shop,
	'shops': shops,
	'total_shops': total_shops,
	'products': products,
	}

	return render(request, 'public/shop.html', context)

def product(request, id):
	product=Product.objects.get(pk=id)
	products = Product.objects.filter(name__contains=product.name, status=1).exclude(id=product.id).order_by('-id')
	paginator = Paginator(products, 3)
	page = request.GET.get('page')
	products = paginator.get_page(page)
	context = {
	'title': product.name,
	'head': product.name,
	'product': product,
	'products': products,
	}

	return render(request, 'public/product.html', context)