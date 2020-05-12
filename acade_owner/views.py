from django.shortcuts import render
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
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import  Q, Count
from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	CreateView
	)
from .models import*
from users.models import*
from .forms import*
from django.db import IntegrityError
from django.db.models import Sum
class AcadeCreateView(LoginRequiredMixin, CreateView):
	model = Acade
	fields = ['name','constructor','address','year','no_of_floors','no_of_rooms','photo']
	def get_context_data(self, **kwargs):
		context = super(AcadeCreateView, self).get_context_data(**kwargs)
		acades = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["acades"] = acades
		context["title"] = "Acades"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have added {name} Building')
			except IntegrityError:
				name = form.cleaned_data.get('name')
				messages.warning(self.request, f'You have ALREADY added {name} Building! May be add another Building')
			else:
				pass
			finally:
				pass
			return redirect('acade')

class AcadeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Acade
	fields = ['name','constructor','address','year','no_of_floors','no_of_rooms']
	def get_context_data(self, **kwargs):
		context = super(AcadeUpdateView, self).get_context_data(**kwargs)
		acades = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["acades"] = acades
		context["title"] = "Acades"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			name = form.cleaned_data.get('name')
			messages.success(self.request, f'Thank you! You have Updated {name} Building')
			return redirect('acade')
	def test_func(self):
		acade = self.get_object()
		if self.request.user == acade.user:
			return True
		return False

class AcadeListView(LoginRequiredMixin, ListView):
	model = Acade
	def get_context_data(self, **kwargs):
		context = super(AcadeListView, self).get_context_data(**kwargs)
		acades = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["acades"] = acades
		context["title"] = "Acades"
		return context

class AcadeDetailView(LoginRequiredMixin, DetailView):
	model = Acade
	def get_context_data(self, **kwargs):
		context = super(AcadeDetailView, self).get_context_data(**kwargs)
		acade = self.get_object()
		page = self.request.GET.get('page')
		context["title"] = "Acades"
		acades = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["acades"] = acades
		employees = Paginator(Employee.objects.filter(acade=acade).order_by('status','-id'), 12)
		context["employees"] = employees.get_page(page)
		rooms = Room.objects.filter(acade=acade).order_by('status','-id')
		context["rooms"] = rooms
		free_rooms = Room.objects.filter(acade=acade, status=1).order_by('-id')
		context["free_rooms"] = free_rooms
		rents = Rent.objects.filter(room__acade=acade).order_by('-id')
		context["rents"] = rents
		bills = Bill.objects.filter(acade=acade).order_by('-id')
		context["bills"] = bills
		tenants = Book.objects.filter(room__acade=acade, status=2, tenant_status=1, ).order_by('-id')
		context["tenants"] = tenants
		complains = Complain.objects.filter(room__room__acade=acade, ).order_by('-id')
		context["complains"] = complains
		visitors = Visitor.objects.filter(acade=acade, ).order_by('-id')
		context["visitors"] = visitors
		total_rent = Rent.objects.filter(room__acade=acade, 
			date_created__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).aggregate(Sum('amount_paid'))['amount_paid__sum']
		total_bills = Bill.objects.filter(acade=acade, 
			date_created__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).aggregate(Sum('amount_paid'))['amount_paid__sum']
		context["collected"] = total_rent
		context["bill_paid"] = total_bills
		return context

class OwnerCreateView(LoginRequiredMixin, CreateView):
	model = Owner
	fields = ['acade','floor','no_of_rooms','name','address','email','phone','photo']
	def get_context_data(self, **kwargs):
		context = super(OwnerCreateView, self).get_context_data(**kwargs)
		owners = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["owners"] = owners
		context["title"] = "Owners"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have added {name} as floor Owner')
			except IntegrityError:
				name = form.cleaned_data.get('name')
				messages.warning(self.request, f'You have ALREADY added Flow Owner {name}! May be you want to add another one ')
			else:
				pass
			finally:
				pass
			return redirect('owner')

class OwnerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Owner
	fields = ['acade','floor','no_of_rooms','name','address','email','phone','photo','status']
	def get_context_data(self, **kwargs):
		context = super(OwnerUpdateView, self).get_context_data(**kwargs)
		owners = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["owners"] = owners
		context["title"] = "Owners"
		return context
	def form_valid(self, form):
		if form.is_valid():
			form.instance.user = self.request.user
			form.save()
			name = form.cleaned_data.get('name')
			messages.success(self.request, f'Thank you! You have Updated {name}')
			return redirect('owner')
	def test_func(self):
		owner = self.get_object()
		if self.request.user == owner.user:
			return True
		return False

class OwnerListView(LoginRequiredMixin, ListView):
	model = Owner
	def get_context_data(self, **kwargs):
		context = super(OwnerListView, self).get_context_data(**kwargs)
		owners = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["owners"] = owners
		context["title"] = "Owners"
		context["head"] = "All"
		return context

class CurrentOwnerListView(LoginRequiredMixin, ListView):
	model = Owner
	def get_context_data(self, **kwargs):
		context = super(CurrentOwnerListView, self).get_context_data(**kwargs)
		owners = self.model.objects.filter(user=self.request.user,status=1).order_by('-id')
		context["owners"] = owners
		context["title"] = "Owners"
		context["head"] = "Current"
		return context

class PreviousOwnerListView(LoginRequiredMixin, ListView):
	model = Owner
	def get_context_data(self, **kwargs):
		context = super(PreviousOwnerListView, self).get_context_data(**kwargs)
		owners = self.model.objects.filter(user=self.request.user,status=2).order_by('-id')
		context["owners"] = owners
		context["title"] = "Owners"
		context["head"] = "Previous"
		return context

class OwnerDetailView(LoginRequiredMixin, DetailView):
	model = Owner
	def get_context_data(self, **kwargs):
		context = super(OwnerDetailView, self).get_context_data(**kwargs)
		owners = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["owners"] = owners
		context["title"] = "Owners"
		return context

class RoomCreateView(LoginRequiredMixin, CreateView):
	form_class = RoomCreateForm
	template_name = "acade_owner/room_form.html"

	def get_context_data(self, **kwargs):
		context = super(RoomCreateView, self).get_context_data(**kwargs)
		rooms = Room.objects.filter(user=self.request.user).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Rooms"
		return context

	def get_form_kwargs(self):
		kwargs = super(RoomCreateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		form = RoomCreateForm(self.request.POST)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have added room {name}')
			except IntegrityError:
				name = form.cleaned_data.get('name')
				messages.warning(self.request, f'You have ALREADY added Room {name}! May be you want to add another Room ')
			else:
				pass
			finally:
				pass
			return redirect('room')

class RoomUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Room
	form_class = RoomCreateForm
	template_name = "acade_owner/room_form.html"

	def get_context_data(self, **kwargs):
		context = super(RoomUpdateView, self).get_context_data(**kwargs)
		rooms = Room.objects.filter(user=self.request.user).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Rooms"
		object = self.get_object()
		context['object'] = context['books'] = object
		return context

	def get_form_kwargs(self):
		kwargs = super(RoomUpdateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		room = Room.objects.get(pk=self.object.id)
		form = RoomCreateForm(self.request.POST, instance=room)
		if form.is_valid():
			form.save()
			name = form.cleaned_data.get('name')
			messages.success(self.request, f'Thank you! You have updated room {name}')
			return redirect('room')
	def test_func(self):
		room = self.get_object()
		if self.request.user == room.user:
			return True
		return False


class RoomListView(LoginRequiredMixin, ListView):
	model = Room
	def get_context_data(self, **kwargs):
		context = super(RoomListView, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Rooms"
		context["head"] = "All"
		return context

class RentListView(LoginRequiredMixin, ListView):
	model = Rent
	def get_context_data(self, **kwargs):
		context = super(RentListView, self).get_context_data(**kwargs)
		page = self.request.GET.get('page')
		rents = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["rents"] = rents
		context["title"] = "Rent"
		context["head"] = "All"
		return context

class BookingListView(LoginRequiredMixin, ListView):
	model = Book
	template_name = "acade_owner/bookings.html"
	def get_context_data(self, **kwargs):
		context = super(BookingListView, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(room__user=self.request.user).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Tenants"
		context["head"] = "Booked"
		return context

class PendingBookingListView(LoginRequiredMixin, ListView):
	model = Book
	template_name = "acade_owner/bookings.html"
	def get_context_data(self, **kwargs):
		context = super(PendingBookingListView, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(room__user=self.request.user, status=1).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Tenants"
		context["head"] = "Pending Bookings"
		return context

class TenantListView(LoginRequiredMixin, ListView):
	model = Book
	template_name = "acade_owner/tenants.html"
	def get_context_data(self, **kwargs):
		context = super(TenantListView, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(room__user=self.request.user, status=2).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Tenants"
		context["head"] = "All Tenants"
		return context

class CurrentTenantListView(LoginRequiredMixin, ListView):
	model = Book
	template_name = "acade_owner/tenants.html"
	def get_context_data(self, **kwargs):
		context = super(CurrentTenantListView, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(room__user=self.request.user, tenant_status=1, status=2).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Tenants"
		context["head"] = "Current Tenants"
		return context

class PreviousTenantListView(LoginRequiredMixin, ListView):
	model = Book
	template_name = "acade_owner/tenants.html"
	def get_context_data(self, **kwargs):
		context = super(PreviousTenantListView, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(room__user=self.request.user, tenant_status=2, status=2).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Tenants"
		context["head"] = "Previous Tenants"
		return context

class RejectedBookingListView(LoginRequiredMixin, ListView):
	model = Book
	template_name = "acade_owner/bookings.html"
	def get_context_data(self, **kwargs):
		context = super(RejectedBookingListView, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(room__user=self.request.user, status=3).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Tenants"
		context["head"] = "Rejected Bookings"
		return context

class FreeRoomListView(LoginRequiredMixin, ListView):
	model = Room
	def get_context_data(self, **kwargs):
		context = super(FreeRoomListView, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(user=self.request.user,status=1).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Rooms"
		context["head"] = "Free"
		return context

class OccupiedRoomListView(LoginRequiredMixin, ListView):
	model = Room
	def get_context_data(self, **kwargs):
		context = super(OccupiedRoomListView, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(user=self.request.user,status=2).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Rooms"
		context["head"] = "Occupied"
		return context

class UnavailableRoomListView(LoginRequiredMixin, ListView):
	model = Room
	def get_context_data(self, **kwargs):
		context = super(UnavailableRoomListView, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(user=self.request.user,status=3).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Rooms"
		context["head"] = "Unavailable"
		return context

class RoomDetailView(LoginRequiredMixin, DetailView):
	model = Room
	def get_context_data(self, **kwargs):
		context = super(RoomDetailView, self).get_context_data(**kwargs)
		room = self.get_object()
		rooms = self.model.objects.filter(user=self.request.user).order_by('-id')
		context["rooms"] = rooms
		employees = Book.objects.filter(room=room, status=2, ).order_by('tenant_status','-id')
		context["employees"] = employees
		rents = Rent.objects.filter(room=room).order_by('-id')
		context["rents"] = rents
		total_rent = Rent.objects.filter(room=room, 
			date_created__gte=timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).aggregate(Sum('amount_paid'))['amount_paid__sum']
		context["collected"] = total_rent
		complains = Complain.objects.filter(room__room=room, ).order_by('-id')
		context["complains"] = complains
		context["title"] = "Rooms"
		return context

class BookedRoomDetails(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Book
	form_class = ApproveBooking
	template_name = "acade_owner/approve_booking.html"

	def get_context_data(self, **kwargs):
		context = super(BookedRoomDetails, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(room__user=self.request.user).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Rooms"
		context["head"] = "My"
		object = self.get_object()
		context['object'] = context['books'] = object
		return context

	def form_valid(self, form):
		book = Book.objects.get(pk=self.object.id)
		room = Room.objects.get(pk=self.object.room.id)
		form = ApproveBooking(self.request.POST, instance=book)
		r_form = ApproveBooking(self.request.POST, instance=room)
		r_form.fields['status'].widget = forms.HiddenInput()
		if form.is_valid():
			form.save(commit=False)
			b_status = form.cleaned_data.get('status')
			# if b_status == BookStatus.objects.get(pk=2):
			# 	r_form.instance.status = RoomStatus.objects.get(pk=2)
			# r_form.save()
			form.save()
			messages.success(self.request, f'Thank you! You have set the request for {book.room} to {b_status}')
			return redirect('booking')
	def test_func(self):
		book = self.get_object()
		if self.request.user == book.room.user:
			return True
		return False

class TenantDetails(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Book
	form_class = UpdateTenantForm
	template_name = "acade_owner/tenant_details.html"

	def get_context_data(self, **kwargs):
		context = super(TenantDetails, self).get_context_data(**kwargs)
		rooms = self.model.objects.filter(room__user=self.request.user).order_by('-id')
		context["rooms"] = rooms
		context["title"] = "Rooms"
		context["head"] = "My"
		object = self.get_object()
		context['object'] = context['books'] = object
		return context

	def form_valid(self, form):
		book = Book.objects.get(pk=self.object.id)
		room = Room.objects.get(pk=self.object.room.id)
		form = UpdateTenantForm(self.request.POST, instance=book)
		if form.is_valid():
			form.save(commit=False)
			b_status = form.cleaned_data.get('tenant_status')
			form.save()
			messages.success(self.request, f'Thank you! You have set the tenant in {book.room} to {b_status}')
			return redirect('tenants')
	def test_func(self):
		book = self.get_object()
		if self.request.user == book.room.user:
			return True
		return False

@login_required
def rent(request, id):
	if request.method == 'POST':
		room=Room.objects.get(pk=id)
		form = RentCreateForm(request.POST)
		if form.is_valid():
			form.instance.user = request.user
			form.instance.room = room
			form.save(commit=False)
			if room.user == request.user:
				form.save()
				messages.success(request, f'You have added rent for {room}! Add another one')
				return redirect('rooms')
			else:
				return redirect('logout')
	else:
		room=Room.objects.get(pk=id)
		form = RentCreateForm()

	rents = Rent.objects.filter(user=request.user).order_by('-id')
	room=Room.objects.get(pk=id)
	context = {
	'form': form, 
	'title': 'Rent', 
	'head': 'Add',
	'rents': rents,
	'room': room,
	}

	return render(request, 'acade_owner/rent_form.html', context)

@login_required
def update_rent(request, id):
	if request.method == 'POST':
		rent=Rent.objects.get(pk=id)
		form = RentUpdateForm(request.POST, instance=rent)
		if form.is_valid():
			form.instance.user = request.user
			form.save()
			messages.success(request, f'You have updated rent for {rent.room}!')
			return redirect('rooms')
	else:
		rent=Rent.objects.get(pk=id)
		form = RentCreateForm(instance=rent)

	rents = Rent.objects.filter(user=request.user).order_by('-id')
	rent=Rent.objects.get(pk=id)
	context = {
	'form': form, 
	'title': 'Rent', 
	'head': 'Update',
	'rents': rents,
	'rent': rent,
	}

	return render(request, 'acade_owner/rent_form.html', context)

class EmployeeCreateView(LoginRequiredMixin, CreateView):
	model = Employee
	form_class = EmployeeCreateForm
	template_name = "acade_owner/employee_form.html"

	def get_context_data(self, **kwargs):
		context = super(EmployeeCreateView, self).get_context_data(**kwargs)
		employees = Employee.objects.filter(user=self.request.user).order_by('-id')
		context["employees"] = employees
		context["title"] = "Employees"
		return context

	def get_form_kwargs(self):
		kwargs = super(EmployeeCreateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		form = EmployeeCreateForm(self.request.POST)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				acade = form.cleaned_data.get('acade')
				name = form.cleaned_data.get('name')
				messages.success(self.request, f'Thank you! You have added Employee {name} for {acade}')
			except IntegrityError:
				name = form.cleaned_data.get('name')
				messages.warning(self.request, f'You ALREADY have {name} in your database for {acade}!')
			else:
				pass
			finally:
				pass
			return redirect('employee')

class EmployeeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Employee
	form_class = EmployeeCreateForm
	template_name = "acade_owner/employee_form.html"

	def get_context_data(self, **kwargs):
		context = super(EmployeeUpdateView, self).get_context_data(**kwargs)
		employees = Employee.objects.filter(user=self.request.user).order_by('-id')
		context["employees"] = employees
		context["title"] = "Employees"
		return context

	def get_form_kwargs(self):
		kwargs = super(EmployeeUpdateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		employee = Employee.objects.get(pk=self.object.id)
		form = EmployeeCreateForm(self.request.POST, instance=employee)
		if form.is_valid():
			form.save()
			name = form.cleaned_data.get('name')
			messages.success(self.request, f'Thank you! You have updated employee {name}')
			return redirect('employee')
	def test_func(self):
		employee = self.get_object()
		if self.request.user == employee.user:
			return True
		return False

class EmployeeDetailView(LoginRequiredMixin, DetailView):
	model = Employee

	def get_context_data(self, **kwargs):
		context = super(EmployeeDetailView, self).get_context_data(**kwargs)
		employees = Employee.objects.filter(user=self.request.user).order_by('-id')
		context["employees"] = employees
		context["title"] = "Employees"
		return context

class EmployeeListView(LoginRequiredMixin, ListView):
	model = Employee

	def get_context_data(self, **kwargs):
		context = super(EmployeeListView, self).get_context_data(**kwargs)
		employees = Employee.objects.filter(user=self.request.user).order_by('-id')
		context["employees"] = employees
		context["title"] = "Employees"
		return context

class BillCreateView(LoginRequiredMixin, CreateView):
	model = Bill
	form_class = BillCreateForm
	template_name = "acade_owner/bill_form.html"

	def get_context_data(self, **kwargs):
		context = super(BillCreateView, self).get_context_data(**kwargs)
		bills = Bill.objects.filter(user=self.request.user).order_by('-id')
		context["bills"] = bills
		context["title"] = "Bills"
		return context

	def get_form_kwargs(self):
		kwargs = super(BillCreateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		form = BillCreateForm(self.request.POST)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				acade = form.cleaned_data.get('acade')
				name = form.cleaned_data.get('bill_for')
				messages.success(self.request, f'Thank you! You have added bill for {name} for {acade}')
			except IntegrityError:
				name = form.cleaned_data.get('bill_for')
				messages.warning(self.request, f'Error! The bill of {name} for {acade} could not be added! Check the form or contact Admin')
			else:
				pass
			finally:
				pass
			return redirect('bill')

class BillUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Bill
	form_class = BillCreateForm
	template_name = "acade_owner/bill_form.html"

	def get_context_data(self, **kwargs):
		context = super(BillUpdateView, self).get_context_data(**kwargs)
		bills = Bill.objects.filter(user=self.request.user).order_by('-id')
		context["bills"] = bills
		context["title"] = "Bills"
		return context

	def get_form_kwargs(self):
		kwargs = super(BillUpdateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		bill = Bill.objects.get(pk=self.object.id)
		form = BillCreateForm(self.request.POST, instance=bill)
		if form.is_valid():
			form.save()
			name = form.cleaned_data.get('bill_for')
			messages.success(self.request, f'Thank you! You have updated bill for {name}')
			return redirect('bill')
	def test_func(self):
		bill = self.get_object()
		if self.request.user == bill.user:
			return True
		return False

class BillDetailView(LoginRequiredMixin, DetailView):
	model = Bill

	def get_context_data(self, **kwargs):
		context = super(BillDetailView, self).get_context_data(**kwargs)
		bills = Bill.objects.filter(user=self.request.user).order_by('-id')
		context["bills"] = bills
		context["title"] = "Bills"
		return context

class BillListView(LoginRequiredMixin, ListView):
	model = Bill

	def get_context_data(self, **kwargs):
		context = super(BillListView, self).get_context_data(**kwargs)
		bills = Bill.objects.filter(user=self.request.user).order_by('-id')
		context["bills"] = bills
		context["title"] = "Bills"
		return context

class VisitorCreateView(LoginRequiredMixin, CreateView):
	model = Visitor
	form_class = VisitorCreateForm
	template_name = "acade_owner/visitor_form.html"

	def get_context_data(self, **kwargs):
		context = super(VisitorCreateView, self).get_context_data(**kwargs)
		visitors = Visitor.objects.filter(user=self.request.user).order_by('-id')
		context["visitors"] = visitors
		context["title"] = "Visitors"
		return context

	def get_form_kwargs(self):
		kwargs = super(VisitorCreateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		form = VisitorCreateForm(self.request.POST)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				acade = form.cleaned_data.get('acade')
				name = form.cleaned_data.get('means')
				messages.success(self.request, f'Thank you! You have added the Visitor by {name} for {acade}')
			except IntegrityError:
				name = form.cleaned_data.get('means')
				messages.warning(self.request, f'Error! The Visitor by {name} could not be added! Check the form or contact Admin')
			else:
				pass
			finally:
				pass
			return redirect('visitor')

class VisitorUpdateView(LoginRequiredMixin, UpdateView):
	model = Visitor
	form_class = VisitorCreateForm
	template_name = "acade_owner/visitor_form.html"

	def get_context_data(self, **kwargs):
		context = super(VisitorUpdateView, self).get_context_data(**kwargs)
		visitors = Visitor.objects.filter(user=self.request.user).order_by('-id')
		context["visitors"] = visitors
		context["title"] = "Visitors"
		return context

	def get_form_kwargs(self):
		kwargs = super(VisitorUpdateView,self).get_form_kwargs()
		kwargs['user'] = self.request.user
		return kwargs

	def form_valid(self, form):
		form = VisitorCreateForm(self.request.POST)
		if form.is_valid():
			form.instance.user = self.request.user
			try:
				form.save()
				acade = form.cleaned_data.get('acade')
				name = form.cleaned_data.get('means')
				messages.success(self.request, f'Thank you! You have updated the Visitor by {name} for {acade}')
			except IntegrityError:
				name = form.cleaned_data.get('means')
				messages.warning(self.request, f'Error! The Visitor by {name} could not be updated! Check the form or contact Admin')
			else:
				pass
			finally:
				pass
			return redirect('visitor')

@login_required
def visitors(request):
	visitors = Visitor.objects.filter(user=request.user).order_by('-id')
	car = Visitor.objects.filter(means=1).count()
	mtb = Visitor.objects.filter(means=2).count()
	bc = Visitor.objects.filter(means=3).count()
	foot = Visitor.objects.filter(means=4).count()
	context = {
	'title': 'Visitors', 
	'head': 'All',
	'visitors': visitors,
	'cars': car,
	'motorcycles': mtb,
	'bicycles': bc,
	'foot': foot,
	}

	return render(request, 'acade_owner/visitors.html', context)

@login_required
def bill_report(request):
	if request.method == 'POST':
		return redirect('selected-bills-report')
	bills = Bill.objects.filter(user=request.user).order_by('-id')
	types = BillType.objects.all()
	arcades = Acade.objects.filter(user=request.user).order_by('-id')
	context = {
	'title': 'Reports',
	'bills': bills,
	'types': types,
	'arcades': arcades,
	}
	return render(request, 'acade_owner/bills_report.html', context)

@login_required
def selected_bill_report(request):
	if request.method == 'POST':
		return redirect('selected-bills-report')

	bills = None
	the_acade = None
	the_bill_for = None
	bill_from = None
	bill_to = None
	acade=request.GET.get('acade', None) 
	bill_from=request.GET.get('bill_from', None)
	bill_to=request.GET.get('bill_to', None)
	bill_for=request.GET.get('bill_for', None)

	try:
		the_acade = Acade.objects.get(id=request.GET.get('acade', None))
		the_bill_for = BillType.objects.get(id=request.GET.get('bill_for', None))
		bills = Bill.objects.filter(
			user=request.user, 
			acade=acade, 
			bill_from__gte=bill_from,
			bill_to__lte=bill_to,
			bill_for=bill_for,
			).order_by('-id')
	except Exception:
		the_acade = Acade.objects.get(id=request.GET.get('acade', None))
		the_bill_for = BillType.objects.get(id=request.GET.get('bill_for', None))
		messages.warning(request, f'I tried to filter but You did not select some values! Please choose the values to select the report you want')
		bills = Bill.objects.filter(
			user=request.user, 
			acade=acade,
			bill_for=bill_for,
			).order_by('-id')
	types = BillType.objects.all()
	arcades = Acade.objects.filter(user=request.user).order_by('-id')
	context = {
	'title': 'Reports',
	'bills': bills,
	'types': types,
	'arcades': arcades,
	'acade': the_acade,
	'bill_to': bill_to,
	'bill_from': bill_from,
	'bill_for': the_bill_for,
	}
	return render(request, 'acade_owner/bills_report.html', context)

@login_required
def rent_report(request):
	if request.method == 'POST':
		return redirect('selected-rent-report')
	rents = Rent.objects.filter(user=request.user).annotate(tamount=Sum('amount_paid')).order_by('-id')
	arcades = Acade.objects.filter(user=request.user).order_by('-id')
	context = {
	'title': 'Reports',
	'rents': rents,
	'arcades': arcades,
	}
	return render(request, 'acade_owner/rents_report.html', context)

@login_required
def selected_rent_report(request):
	if request.method == 'POST':
		return redirect('selected-rents-report')

	rents = None
	the_acade = None
	rent_from = None
	rent_to = None
	acade=request.GET.get('acade', None)
	rent_from=request.GET.get('rent_from', None)
	rent_to=request.GET.get('rent_to', None)

	try:
		the_acade = Acade.objects.get(id=request.GET.get('acade', None))
		rents = Rent.objects.filter(
			user=request.user, 
			room__acade=acade, 
			rent_from__gte=rent_from,
			rent_to__lte=rent_to,
			).order_by('-id')
	except Exception:
		the_acade = Acade.objects.get(id=request.GET.get('acade', None))
		messages.warning(request, f'I tried to filter but You did not select some values! Please choose the values to select the report you want')
		rents = Rent.objects.filter(
			user=request.user, 
			room__acade=acade,
			).order_by('-id')
	arcades = Acade.objects.filter(user=request.user).order_by('-id')
	context = {
	'title': 'Reports',
	'rents': rents,
	'arcades': arcades,
	'acade': the_acade,
	'rent_from': rent_from,
	'rent_to': rent_to,
	}
	return render(request, 'acade_owner/rents_report.html', context)

def default_home(request):
	products = Product.objects.filter(status=1).order_by('-id')
	paginator = Paginator(products, 10)
	page = request.GET.get('page')
	products = paginator.get_page(page)
	context = {
	'title': 'Home',
	'products': products,
	}

	return render(request, 'acade_owner/base.html', context)


def home(request):
	shops = Shop.objects.all().order_by('-id')
	rooms = Room.objects.filter(status=1).order_by('-id')
	acades = Acade.objects.annotate(number_of_rooms=Count('room', filter=Q(room__status=1)), number_of_shops=Count('room__book__shop')).order_by('-number_of_rooms','-number_of_shops')
	products = Product.objects.filter(status=1).order_by('-id')
	paginator = Paginator(products, 3)
	page = request.GET.get('page')
	products = paginator.get_page(page)

	rent_amount = None
	room_count = None
	book_count = None
	complain_count = None
	free_room_count = None
	if request.user.is_authenticated:
		room_count = Room.objects.filter(user=request.user).count()
		free_room_count = Room.objects.filter(user=request.user, status=1).count()
		book_count = Book.objects.filter(room__user=request.user, status=1).count()
		complain_count = Complain.objects.filter(room__room__user=request.user).count()
	context = {
	'title': 'Home',
	'products': products,
	'shops': shops,
	'acades': acades,
	'rooms': rooms,
	'room_count': room_count,
	'book_count': book_count,
	'complain_count': complain_count,
	'free_room_count': free_room_count,
	}
	return render(request, 'acade_owner/home.html', context)

@login_required
def room_chart(request):
	labels = []
	data = []
	rooms = Rent.objects.values('room__name').filter(user=request.user).annotate(total_rent=Sum('amount_paid')).order_by('-total_rent')
	for room in rooms:
		labels.append(room['room__name'])
		data.append(room['total_rent'])

	return JsonResponse(data={'labels': labels, 'data': data, })