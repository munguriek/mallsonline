from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from acade_owner.models import*

class BookStatus(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class TenantStatus(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class ProductStatus(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class ComplainType(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	photo = models.ImageField(default='user_photos/default.png', upload_to='user_photos', blank=True, null=True,)
	address = models.CharField(max_length=200, blank=True, null=True)
	phone = models.CharField(max_length=200, blank=True, null=True)
	updated = models.DateTimeField(auto_now=True)
	def __str__(self):
		return f'{self.user.first_name} {self.user.last_name}'

class Book(models.Model):
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	occupation = models.CharField(max_length=200)
	business = models.CharField(max_length=200, verbose_name='Business intented to use the room for')
	person = models.CharField(max_length=200, verbose_name='Contact Person')
	phone = models.CharField(max_length=200, verbose_name='Contact Phone')
	address = models.CharField(max_length=200, verbose_name='Contact Address')
	comment = models.TextField(verbose_name='Add a comment')
	approve_comment = models.CharField(max_length=1000, verbose_name='Add a comment')
	status = models.ForeignKey(BookStatus, default=1, on_delete=models.SET_DEFAULT, verbose_name='Booking Status')
	tenant_status = models.ForeignKey(TenantStatus, default=1, on_delete=models.SET_DEFAULT)
	date_created = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return f'{self.user.first_name} {self.user.last_name}, {self.room}'

	class Meta():
		unique_together=['user','room']

class Complain(models.Model):
	room = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Room of Complain',)
	complain_type = models.ForeignKey(ComplainType, default=1, on_delete=models.SET_DEFAULT, verbose_name='Visible by',)
	date_created = models.DateTimeField(default=timezone.now)
	title = models.CharField(max_length=200, verbose_name='Complain Title')
	body = models.TextField(verbose_name='Complain Body')
	updated = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return f'{self.room.room}, {self.title}'

class Comment(models.Model):
	complain = models.ForeignKey(Complain, on_delete=models.CASCADE,)
	date_created = models.DateTimeField(default=timezone.now)
	body = models.TextField(verbose_name='Comment')
	updated = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return f'{self.user}`s Comment on {self.complain}`'

class Shop(models.Model):
	room = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Room of Shop',)
	date_created = models.DateTimeField(default=timezone.now)
	name = models.CharField(max_length=200, verbose_name='Shop Name')
	title = models.CharField(max_length=200, verbose_name='Business type')
	body = models.TextField(verbose_name='Business description')
	photo = models.ImageField(default='shop_photos/default.png', upload_to='shop_photos', blank=True, null=True,)
	updated = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return self.name

class Product(models.Model):
	shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Shop of the Product',)
	date_created = models.DateTimeField(default=timezone.now)
	name = models.CharField(max_length=200, verbose_name='Product Name')
	body = models.TextField(verbose_name='Product description')
	cost = models.IntegerField(verbose_name='Buying Cost')
	price = models.IntegerField(verbose_name='Selling Price')
	actual_price = models.IntegerField(verbose_name='Sold at', blank=True, null=True,)
	status = models.ForeignKey(ProductStatus, default=1, on_delete=models.SET_DEFAULT)
	photo = models.ImageField(default='phoduct_photos/default.png', upload_to='product_photos', blank=True, null=True,)
	updated = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return self.name