from django.shortcuts import render,  redirect
from django.db.models.signals import post_save
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import *
from .models import *
from acade_owner.models import *
from django.db import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	CreateView
	)

def login_success(request):
	usergroup = None
	if request.user.is_authenticated:
		usergroup = request.user.groups.values_list('id', flat=True).last()
	if usergroup == settings.OWNER_GROUP_ID:
		return redirect('owner-home')
	if usergroup == settings.SHOP_OWNER_GROUP_ID:
		return redirect('users-home')
	else:
		return redirect('public-home')

@login_required
def updateprofile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
		if u_form.is_valid() and u_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Thank you! Your profile has been updated')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = UserProfileUpdateForm(instance=request.user.userprofile)

	context = {
	'u_form':u_form,
	'p_form':p_form,
	'title': 'Home'
	}
	return render(request, 'users/profile.html', context)

class ProfileListView(ListView):
	model = UserProfile
	context_object_name = 'profiles'
	ordering = ['-id']

@login_required
def profile(request):
	context = {
	'title': 'Home'
	}
	return render(request, 'users/userprofile_detail.html', context)

@login_required
def users_home(request):
	return render(request, 'users/home.html', {'title': 'Home'})

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			group = Group.objects.get(pk=settings.PUBLIC_GROUP_ID)
			user.groups.add(group)
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'acade_owner/base.html', {'form': form, 'title': 'Register'})

class FreeRooms(ListView):
	model = Room
	template_name = "users/free_rooms.html"
	def get_context_data(self, **kwargs):
		context = super(FreeRooms, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(status=1).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Free Rooms"
		context["head"] = "Free"
		return context

class MyRooms(ListView):
	model = Book
	template_name = "users/book_list.html"
	def get_context_data(self, **kwargs):
		context = super(MyRooms, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Free Rooms"
		context["head"] = "My"
		return context

@login_required
def book_room(request, id):
	if request.method == 'POST':
		room=Room.objects.get(pk=id)
		form = BookRoomCreateForm(request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.instance.room = room
			try:
				form.save()
				messages.success(request, f'You have BOOKED {room}!')
			except IntegrityError:
				messages.warning(request, f'You have ALREADY BOOKED {room}! May be Look for another room')
			else:
				pass
			finally:
				pass
			return redirect('users-free-rooms')
	else:
		room=Room.objects.get(pk=id)
		form = BookRoomCreateForm(instance=room)

	rooms = Book.objects.filter(user=request.user).order_by('-id')
	return render(request, 'users/book_form.html', {'form': form, 'title': 'Free Rooms', 'rooms': rooms})

@login_required
def update_book_room(request, id):
	if request.method == 'POST':
		room=Book.objects.get(pk=id)
		form = BookRoomUpdateForm(request.POST, instance=room)
		if form.is_valid():
			form.save()
			return redirect('my-rooms')
	else:
		room=Book.objects.get(pk=id)
		form = BookRoomUpdateForm(instance=room)

	rooms = Book.objects.filter(user=request.user).order_by('-id')
	return render(request, 'users/book_form.html', {'form': form, 'title': 'Free Rooms', 'rooms': rooms})


class MyRoomDetails(DetailView):
	model = Book
	def get_context_data(self, **kwargs):
		context = super(MyRoomDetails, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(user=self.request.user, status=1).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Free Rooms"
		context["head"] = "My"
		return context

class RoomDetails(DetailView):
	model = Room
	template_name = "users/room_detail.html"
	def get_context_data(self, **kwargs):
		context = super(RoomDetails, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(user=self.request.user, status=1).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Free Rooms"
		context["head"] = "My"
		return context

class ComplainCreateView(LoginRequiredMixin, CreateView):
	model = Complain
	form_class = ComplainCreateForm
	template_name = "users/complain_form.html"

	def get_context_data(self, **kwargs):
		context = super(ComplainCreateView, self).get_context_data(**kwargs)
		complains = Complain.objects.filter(user=self.request.user).order_by('-id')
		context["complains"] = complains
		context["title"] = "Complains"
		return context

	def get_form_kwargs(self):
		kwargs = super(ComplainCreateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		form = ComplainCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('title')
				messages.success(self.request, f'Thank you! You have raised {name} complain')
			except IntegrityError:
				name = form.cleaned_data.get('title')
				messages.warning(self.request, f'Error! {name} Failed! Check the form or contact Admin')
			else:
				pass
			finally:
				pass
			return redirect('complain')

class ComplainUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Complain
	form_class = ComplainCreateForm
	template_name = "users/complain_form.html"

	def get_context_data(self, **kwargs):
		context = super(ComplainUpdateView, self).get_context_data(**kwargs)
		complains = Complain.objects.filter(user=self.request.user).order_by('-id')
		context["complains"] = complains
		context["title"] = "Complains"
		return context

	def get_form_kwargs(self):
		kwargs = super(ComplainUpdateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		complain = Complain.objects.get(pk=self.object.id)
		form = ComplainCreateForm(self.request.POST, self.request.FILES, instance=complain)
		if form.is_valid():
			form.save()
			name = form.cleaned_data.get('title')
			messages.success(self.request, f'Thank you! You have updated the {name} Complain')
			return redirect('complain')
	def test_func(self):
		complain = self.get_object()
		if self.request.user == complain.user:
			return True
		return False

class MyComplainsListView(ListView):
	model = Complain
	def get_context_data(self, **kwargs):
		context = super(MyComplainsListView, self).get_context_data(**kwargs)
		complains = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["complains"] = complains
		context["title"] = "Complains"
		context["head"] = "My"
		return context

class TenantComplainsListView(ListView):
	model = Complain
	def get_context_data(self, **kwargs):
		context = super(TenantComplainsListView, self).get_context_data(**kwargs)
		complains = self.model.objects.filter(complain_type=1).order_by('-id')
		context["complains"] = complains
		context["title"] = "Complains"
		context["head"] = "My"
		return context

class AllComplainsListView(ListView):
	model = Complain
	def get_context_data(self, **kwargs):
		context = super(AllComplainsListView, self).get_context_data(**kwargs)
		complains = self.model.objects.filter(room__room__user=self.request.user).order_by('-id')
		context["complains"] = complains
		context["title"] = "Complains"
		context["head"] = "All"
		return context

@login_required
def comment(request, id):
	if request.method == 'POST':
		complain=Complain.objects.get(pk=id)
		form = CommentCreateForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.user = request.user
			form.instance.complain = complain
			form.save()
			messages.success(request, f'You have shared your view')
			return HttpResponseRedirect(reverse('complain-details', kwargs={'id':id}))

	else:
		complain=Complain.objects.get(pk=id)
		form = CommentCreateForm()
	complain=Complain.objects.get(pk=id)
	comments = Comment.objects.filter(complain=complain).order_by('-id')
	total_comments = Comment.objects.filter(complain=complain).count()
	paginator = Paginator(comments, 5)
	page = request.GET.get('page')
	comments = paginator.get_page(page)
	complains = Complain.objects.filter(user=request.user).order_by('-id')
	paginator = Paginator(complains, 10)
	page = request.GET.get('page')
	complains = paginator.get_page(page)
	context = {
	'form': form, 
	'title': 'Complains', 
	'head': 'Add',
	'comments': comments,
	'total_comments': total_comments,
	'complain': complain,
	'complains': complains,
	}

	return render(request, 'users/complain_detail.html', context)

@login_required
def update_comment(request, id):
	if request.method == 'POST':
		comment=Comment.objects.get(pk=id)
		form = CommentCreateForm(request.POST, request.FILES, instance=comment)
		if form.is_valid():
			comment=Comment.objects.get(pk=id)
			if comment.user == request.user:
				form.save()
				messages.success(request, f'You have updated your comment')
				return HttpResponseRedirect(reverse('complain-details', kwargs={'id':comment.complain.id}))
			else:
				return HttpResponseRedirect(reverse('complain-details', kwargs={'id':comment.complain.id}))
	else:
		comment=Comment.objects.get(pk=id)
		form = CommentCreateForm(instance=comment)
	comment=Comment.objects.get(pk=id)
	complain=Complain.objects.get(pk=comment.complain.id)
	comments = Comment.objects.filter(complain=complain).order_by('-id')
	total_comments = Comment.objects.filter(complain=complain).count()
	paginator = Paginator(comments, 5)
	page = request.GET.get('page')
	comments = paginator.get_page(page)
	complains = Complain.objects.filter(user=request.user).order_by('-id')
	paginator = Paginator(complains, 10)
	page = request.GET.get('page')
	complains = paginator.get_page(page)
	context = {
	'form': form, 
	'title': 'Complains', 
	'head': 'Add',
	'comments': comments,
	'total_comments': total_comments,
	'complain': complain,
	'complains': complains,
	}

	return render(request, 'users/complain_detail.html', context)

	
class ShopCreateView(LoginRequiredMixin, CreateView):
	model = Shop
	form_class = ShopCreateForm
	template_name = "users/shop_form.html"

	def get_context_data(self, **kwargs):
		context = super(ShopCreateView, self).get_context_data(**kwargs)
		shops = Shop.objects.filter(user=self.request.user).order_by('-id')
		context["shops"] = shops
		context["title"] = "Shops"
		return context

	def get_form_kwargs(self):
		kwargs = super(ShopCreateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		form = ShopCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have created {name}')
			except IntegrityError:
				name = form.cleaned_data.get('name')
				messages.warning(self.request, f'Error! {name} Failed! Check the form or contact Admin')
			else:
				pass
			finally:
				pass
			return redirect('shop')

class ShopUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Shop
	form_class = ShopCreateForm
	template_name = "users/shop_form.html"

	def get_context_data(self, **kwargs):
		context = super(ShopUpdateView, self).get_context_data(**kwargs)
		shops = Shop.objects.filter(user=self.request.user).order_by('-id')
		context["shops"] = shops
		context["title"] = "Shops"
		return context

	def get_form_kwargs(self):
		kwargs = super(ShopUpdateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		shop = Shop.objects.get(pk=self.object.id)
		form = ShopCreateForm(self.request.POST, self.request.FILES, instance=shop)
		if form.is_valid():
			form.save()
			name = form.cleaned_data.get('name')
			messages.success(self.request, f'Thank you! You have updated the {name}')
			return redirect('shop')
	def test_func(self):
		shop = self.get_object()
		if self.request.user == shop.user:
			return True
		return False

class MyShopListView(ListView):
	model = Shop
	def get_context_data(self, **kwargs):
		context = super(MyShopListView, self).get_context_data(**kwargs)
		shops = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["shops"] = shops
		context["title"] = "Shops"
		context["head"] = "My"
		return context

class AllShopListView(ListView):
	model = Shop
	def get_context_data(self, **kwargs):
		context = super(AllShopListView, self).get_context_data(**kwargs)
		shops = self.model.objects.all().order_by('-id')
		context["shops"] = shops
		context["title"] = "Shops"
		context["head"] = "All"
		return context

class ShopDetailView(DetailView):
	model = Shop
	def get_context_data(self, **kwargs):
		context = super(ShopDetailView, self).get_context_data(**kwargs)
		shops = self.model.objects.all().order_by('-id')
		products = Product.objects.filter(shop=self.get_object()).order_by('-id')
		context["shops"] = shops
		context["products"] = products
		context["title"] = "Shops"
		context["head"] = "All"
		return context

class ProductCreateView(LoginRequiredMixin, CreateView):
	model = Product
	form_class = ProductCreateForm
	template_name = "users/product_form.html"

	def get_context_data(self, **kwargs):
		context = super(ProductCreateView, self).get_context_data(**kwargs)
		products = Product.objects.filter(user=self.request.user).order_by('-id')
		context["products"] = products
		context["title"] = "Products"
		return context

	def get_form_kwargs(self):
		kwargs = super(ProductCreateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		form = ProductCreateForm(self.request.POST, self.request.FILES)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have Added {name}')
			except IntegrityError:
				name = form.cleaned_data.get('name')
				messages.warning(self.request, f'Error! {name} Failed! Check the form or contact Admin')
			else:
				pass
			finally:
				pass
			return redirect('product')

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Product
	form_class = ProductUpdateForm
	template_name = "users/product_form.html"

	def get_context_data(self, **kwargs):
		context = super(ProductUpdateView, self).get_context_data(**kwargs)
		products = Product.objects.filter(user=self.request.user).order_by('-id')
		context["products"] = products
		context["title"] = "Products"
		return context

	def get_form_kwargs(self):
		kwargs = super(ProductUpdateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		product = Product.objects.get(pk=self.object.id)
		form = ProductUpdateForm(self.request.POST, self.request.FILES, instance=product)
		if form.is_valid():
			form.save()
			name = form.cleaned_data.get('name')
			messages.success(self.request, f'Thank you! You have updated {name}')
			return redirect('product')
	def test_func(self):
		product = self.get_object()
		if self.request.user == product.user:
			return True
		return False

class MyProductListView(ListView):
	model = Product
	def get_context_data(self, **kwargs):
		context = super(MyProductListView, self).get_context_data(**kwargs)
		products = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["products"] = products
		context["title"] = "Products"
		context["head"] = "My"
		return context

class AllProductListView(ListView):
	model = Product
	def get_context_data(self, **kwargs):
		context = super(AllProductListView, self).get_context_data(**kwargs)
		products = self.model.objects.all().order_by('-id')
		context["products"] = products
		context["title"] = "Products"
		context["head"] = "All"
		return context

class ProductDetailView(DetailView):
	model = Product
	def get_context_data(self, **kwargs):
		context = super(ProductDetailView, self).get_context_data(**kwargs)
		products = self.model.objects.all().order_by('-id')
		context["products"] = products
		context["title"] = "Products"
		context["head"] = "All"
		return context