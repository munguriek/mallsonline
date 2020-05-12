from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=200)
	last_name = forms.CharField(max_length=200)
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=200)
	last_name = forms.CharField(max_length=200)
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email']

class UserProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['address','phone','photo']

class BookRoomCreateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(BookRoomCreateForm,self).__init__(*args,**kwargs)

	class Meta:
		model = Book
		fields = ('person','phone','occupation','address','business','comment')

class BookRoomUpdateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(BookRoomUpdateForm,self).__init__(*args,**kwargs)

	class Meta:
		model = Book
		fields = ('person','phone','occupation','address','business','comment')

class ComplainCreateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(ComplainCreateForm,self).__init__(*args,**kwargs)
		if user is not None:
			self.fields['room'].queryset = Book.objects.filter(user=user, status=2)

	class Meta:
		model = Complain
		fields = ('room','title','body',)

class CommentCreateForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ('body',)
		widgets = {
		'body':forms.Textarea(attrs={'rows': 2, 'cols': 40})
		}

class ShopCreateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(ShopCreateForm,self).__init__(*args,**kwargs)
		if user is not None:
			self.fields['room'].queryset = Book.objects.filter(user=user, status=2, tenant_status=1)

	class Meta:
		model = Shop
		fields = ('room','name','title','body','photo',)

class ProductCreateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(ProductCreateForm,self).__init__(*args,**kwargs)
		if user is not None:
			self.fields['shop'].queryset = Shop.objects.filter(user=user)

	class Meta:
		model = Product
		fields = ('shop','name','body','cost','price','photo',)

class ProductUpdateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super(ProductUpdateForm,self).__init__(*args,**kwargs)
		if user is not None:
			self.fields['shop'].queryset = Shop.objects.filter(user=user)

	class Meta:
		model = Product
		fields = ('shop','name','body','cost','price','status','actual_price','photo',)