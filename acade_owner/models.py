from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator 

class Year(models.Model):
	year = models.IntegerField()
	def __str__(self):
		return f'{self.year}'

class Month(models.Model):
	month = models.CharField(max_length=200)
	def __str__(self):
		return self.month

class Floor(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class RoomSize(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class RoomStatus(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class OwnerStatus(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class BillType(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class Mean(models.Model):
	name = models.CharField(max_length=200)
	def __str__(self):
		return self.name

class Builder(models.Model):
	name = models.CharField(max_length=200, verbose_name='Building Constructor')
	photo = models.ImageField(default='constructor_photos/default.png', upload_to='constructor_photos', blank=True, null=True,)
	year = models.ForeignKey(Year, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Year Established')
	address = models.CharField(max_length=200, blank=True, null=True, verbose_name='Constructor Address')
	date_created = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return self.name

class Acade(models.Model):
	name = models.CharField(max_length=200, verbose_name='Acade Name')
	no_of_floors = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
	no_of_rooms = models.IntegerField(validators=[MinValueValidator(1)])
	photo = models.ImageField(default='acade_photos/default.png', upload_to='acade_photos', blank=True, null=True,)
	year = models.ForeignKey(Year, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Year of Construction')
	address = models.CharField(max_length=200, blank=True, null=True, verbose_name='Acade Address')
	constructor = models.ForeignKey(Builder, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Constructor')
	date_created = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return self.name
	class Meta():
		unique_together=['user','name']
		
class Room(models.Model):
	acade = models.ForeignKey(Acade, on_delete=models.CASCADE, verbose_name='Building')
	floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name='Floor')
	name = models.CharField(max_length=200, verbose_name='Room Name')
	size = models.ForeignKey(RoomSize, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='Room Size')
	status = models.ForeignKey(RoomStatus, default=1, on_delete=models.SET_DEFAULT, verbose_name='Room Status')
	monthly_rate = models.IntegerField(validators=[MinValueValidator(50000)])
	date_created = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return f'{self.acade} {self.floor}, {self.name}'
	class Meta():
		unique_together=['user','acade','floor','name']

class Owner(models.Model):
	acade = models.ForeignKey(Acade, on_delete=models.CASCADE, verbose_name='Building')
	floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name='Floor Owned')
	no_of_rooms = models.IntegerField()
	name = models.CharField(max_length=200, verbose_name='Owner Name')
	address = models.CharField(max_length=200, verbose_name='Owner Address')
	email = models.CharField(max_length=200, verbose_name='Owner Email Address')
	phone = models.CharField(max_length=200, verbose_name='Owner Phone Number')
	status = models.ForeignKey(OwnerStatus, default=1, on_delete=models.SET_DEFAULT, verbose_name='Owner Status')
	photo = models.ImageField(default='owner_photos/default.png', upload_to='owner_photos', blank=True, null=True,)
	date_created = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return self.name
	class Meta():
		unique_together=['acade','floor','name']

class Rent(models.Model):
	room = models.ForeignKey(Room, on_delete=models.CASCADE, )
	amount_paid = models.IntegerField()
	amount_to_pay = models.IntegerField(verbose_name='Remaining Balance',)
	paid_by = models.CharField(max_length=200,)
	phone = models.CharField(max_length=200, verbose_name='Phone Number')
	rent_from = models.DateField(default=timezone.now)
	rent_to = models.DateField(default=timezone.now)
	date_created = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return f'{self.room}, {self.rent_from} {self.rent_to}'

class Employee(models.Model):
	acade = models.ForeignKey(Acade, on_delete=models.CASCADE, verbose_name='Building')
	name = models.CharField(max_length=200, verbose_name='Employee Name')
	phone = models.CharField(max_length=200, verbose_name='Employee Phone')
	email = models.CharField(max_length=200, blank=True, null=True, verbose_name='Employee Email')
	address = models.CharField(max_length=200, verbose_name='Employee Address')
	nin = models.CharField(max_length=200, verbose_name='National ID No.')
	role = models.CharField(max_length=200, verbose_name='Job Title')
	date_of_birth = models.DateField(default=timezone.now)
	status = models.ForeignKey(OwnerStatus, default=1, on_delete=models.SET_DEFAULT, verbose_name='Employee Status')
	date_created = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	photo = models.ImageField(default='employee_photos/default.png', upload_to='employee_photos', blank=True, null=True,)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return f'{self.acade}, {self.name} {self.nin}'
	class Meta():
		unique_together=['user','acade','nin',]

class Bill(models.Model):
	acade = models.ForeignKey(Acade, on_delete=models.CASCADE, verbose_name='Building',)
	bill_for = models.ForeignKey(BillType, on_delete=models.CASCADE,)
	bill_from = models.DateField(default=timezone.now)
	bill_to = models.DateField(default=timezone.now)
	amount_paid = models.IntegerField()
	amount_to_pay = models.IntegerField(verbose_name='Remaining Balance',)
	paid_by = models.CharField(max_length=200,)
	received_by = models.CharField(max_length=200,)
	phone = models.CharField(max_length=200, verbose_name='Phone Number')
	date_created = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return f'{self.acade}, {self.bill_for}, {self.bill_from} {self.bill_to}'

class Visitor(models.Model):
	means = models.ForeignKey(Mean, default=1, on_delete=models.SET_DEFAULT, verbose_name='Transport Means')
	acade = models.ForeignKey(Acade, default=1, on_delete=models.CASCADE, verbose_name='Building')
	date_created = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	def __str__(self):
		return self.name


