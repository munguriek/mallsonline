from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from users.models import *

class RoomCreateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(RoomCreateForm,self).__init__(*args,**kwargs)
		if user is not None:
			self.fields['acade'].queryset = Acade.objects.filter(user=user)

	class Meta:
		model = Room
		fields = ('acade','floor','name','size','status','monthly_rate')

class EmployeeCreateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(EmployeeCreateForm,self).__init__(*args,**kwargs)
		if user is not None:
			self.fields['acade'].queryset = Acade.objects.filter(user=user)

	class Meta:
		model = Employee
		fields = ('acade','name','role','nin','date_of_birth','phone','email','address','status','photo')

class BillCreateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(BillCreateForm,self).__init__(*args,**kwargs)
		if user is not None:
			self.fields['acade'].queryset = Acade.objects.filter(user=user)

	class Meta:
		model = Bill
		fields = ('acade','bill_for','bill_from','bill_to','amount_paid','amount_to_pay','paid_by','received_by','phone',)

class VisitorCreateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(VisitorCreateForm,self).__init__(*args,**kwargs)
		if user is not None:
			self.fields['acade'].queryset = Acade.objects.filter(user=user)

	class Meta:
		model = Visitor
		fields = ('acade','means',)


class RentCreateForm(forms.ModelForm):

	class Meta:
		model = Rent
		fields = ('rent_from','rent_to','amount_paid','amount_to_pay','paid_by','phone')

class RentUpdateForm(forms.ModelForm):

	class Meta:
		model = Rent
		fields = ('rent_from','rent_to','amount_paid','amount_to_pay','paid_by','phone')

class ApproveBooking(forms.ModelForm):
	approve_comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 40}))

	class Meta:
		model = Book
		fields = ('status','approve_comment')

class UpdateTenantForm(forms.ModelForm):

	class Meta:
		model = Book
		fields = ('tenant_status',)

class UpdateRoom(forms.ModelForm):
	status = models.ForeignKey(RoomStatus, default=1, on_delete=models.SET_DEFAULT, verbose_name='Update Room Status')

	class Meta:
		model = Room
		fields = ('status',)