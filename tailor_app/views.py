from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Customer, Order, Measurement, ExtraMeasurement, Report
from .forms import (CustomerForm, 
EditCustomerForm,
OrderForm, 
MeasurementForm2, 
MeasurementForm, 
ExtraMeasurementForm, 
OrderForm2)

from account.forms import EditUserForm
# Create your views here.

@login_required
def customers_page(request):
    user = request.user
    all_customers=user.customer_set.all()
	
    context = {
    'customers': all_customers,
    'customer_form' : CustomerForm(),
    }
    return render(request, 'tailor_app/customers.html', context)


@login_required	
@api_view(['GET'])
def search_customers(request):	
	filter = request.GET.get('customer_filter')
	customers = request.user.customer_set.filter(name__icontains=filter)
	data = render_to_string("tailor_app/customer_search.html",
	{"customers":customers}, request=request )
	return HttpResponse(data)
	
@login_required	
@api_view(['POST'])
def add_customer(request):	
	customer = CustomerForm(request.POST).save(commit=False)
	customer.tailor = request.user
	customer.save()
	request.user.report_set.create(status = "ADD-CUSTOMER", description = f"New Customer '{customer.name}' added ")
	data = render_to_string("tailor_app/add_customer_data.html", {"customer" : customer}) 
	return HttpResponse(data)	


@login_required	
@api_view(['POST'])
def edit_customer(request):	
	instance = get_object_or_404(Customer,id = request.POST.get("id"))
	customer = CustomerForm(request.POST, instance=instance).save(commit=False)
	customer.save()
	request.user.report_set.create(status = "EDIT-CUSTOMER", description = f"Customer '{customer.name}' data was edited added ")
	return HttpResponse('Success')
	

@login_required	
@api_view(['GET'])
def edit_form_customer(request):
	customer_id = int(request.GET.get("customer_id"))
	customer = get_object_or_404(Customer, tailor = request.user, id=customer_id)
	id = customer.id
	customer_form = EditCustomerForm(instance = customer )
	data = render_to_string("tailor_app/update_customer_data.html", {"customer_form" : customer_form, "id":id}, request=request) 
	return HttpResponse(data)	
	
				

@login_required	
@api_view(['POST'])
def delete_customer(request):	
	customer_id = request.POST.get("customer_id")
	customer = Customer.objects.filter(id=customer_id)
	name = customer[0].name
	customer.delete()
	request.user.report_set.create(status = "DELETE-CUSTOMER", description = f"Customer '{name}' data was deleted  ")
	return HttpResponse('Deleted Successfully!!!')



#######################################  ORDER VIEWS  ################################################

@login_required
def orders_page(request):
    user = request.user
    all_orders=  Order.objects.filter(customer__tailor = user)
    context = {
    'orders': all_orders,
	'order_form' : OrderForm(request=request)
    }
    return render(request, 'tailor_app/orders.html', context)


@login_required	
@api_view(['POST'])
def add_order(request):	
	customer_order = OrderForm(request.POST, request=request).save(commit=False)
	customer_order.save()
	request.user.report_set.create(status = "ADD-ORDER", description = f"New order by '{customer_order.customer}' was added ")
	data = render_to_string("tailor_app/add_order.html", {"order" : customer_order}) 
	return HttpResponse(data)

@login_required	
@api_view(['GET'])
def edit_form_order(request):
	order_id = request.GET.get("order_id")
	order = get_object_or_404(Order, customer__tailor = request.user, tracking_id=order_id)
	id = order.id
	order_form = OrderForm2(instance = order )
	data = render_to_string("tailor_app/update_order_data.html", {"order_form" : order_form, "id":id}, request=request) 
	return HttpResponse(data)


@login_required	
@api_view(['POST'])
def edit_order(request):	
	instance = get_object_or_404(Order,id = request.POST.get("id"))
	order = OrderForm2(request.POST, instance=instance).save(commit=False)
	order.save()
	request.user.report_set.create(status = "EDIT-ORDER", description = f"Order by '{order.customer}' was edited ")
	return HttpResponse('Success')


@login_required	
@api_view(['POST'])
def delete_order(request):	
	order_id = request.POST.get("order_id")
	order = Order.objects.filter(tracking_id=order_id, customer__tailor = request.user)
	name = order.first().customer
	order.delete()
	
	request.user.report_set.create(status = "DELETE-ORDER", description = f"order by '{name}' was deleted ")
	return HttpResponse('Deleted Successfully!!!')


#######################################  MEASUREMENT VIEWS  ################################################

@login_required
def measurements_page(request):
    user = request.user
    all_measurements=  Measurement.objects.filter(customer__tailor = user)
    context = {
    'measurements': all_measurements,
	'measurement_form' : MeasurementForm(request=request),
	'extra_measurement_form' : ExtraMeasurementForm()
    }
    return render(request, 'tailor_app/measurement.html', context)


@login_required	
@api_view(['POST'])
def add_measurement(request):	
	customer_measurement = MeasurementForm(request.POST, request=request).save(commit=False)
	customer_measurement.save()	
	request.user.report_set.create(status = "ADD-MEASUREMENT", 
	description = f"New measurement of '{customer_measurement.customer}' was added ")
	data = render_to_string("tailor_app/add_measurement.html", {"measurement" : customer_measurement})
	return HttpResponse(data)

@login_required	
@api_view(['POST'])
def add_extra_measurement(request):
	measurement_id = int(request.POST.get("measurement"))
	customer_extra_measurement = ExtraMeasurementForm(request.POST).save(commit=False)
	customer_extra_measurement.measurement = get_object_or_404(Measurement, id=measurement_id, customer__tailor = request.user)
	customer_extra_measurement.save()
	request.user.report_set.create(status = "ADD-EXTRA-MEASUREMENT", 
	description = f"New extra measurement of '{customer_extra_measurement.measurement.customer}' was added ")
	data = render_to_string("tailor_app/add_extra_measurement.html", {"measurement" : customer_extra_measurement})
	return HttpResponse(data)

@login_required	
@api_view(['POST'])
def delete_measurement(request):	
	measurement_id = request.POST.get("measurement_id")
	measurement = Measurement.objects.filter(id=measurement_id, customer__tailor = request.user)
	measurement.delete()
	name = measurement[0].customer
	request.user.report_set.create(status = "DELETE-MEASUREMENT", 
	description = f"Measurement of '{name}' was deleted ")
	return HttpResponse('Deleted Successfully!!!')

@login_required	
@api_view(['GET'])
def delete_extra_measurement(request):	
	extra_measurement_id = request.GET.get("extra_measurement_id")
	extra_measurement = ExtraMeasurement.objects.filter(id=extra_measurement_id, measurement__customer__tailor = request.user)
	name = extra_measurement[0].measurement.customer
	extra_measurement.delete()
	request.user.report_set.create(status = "DELETE-EXTRA-MEASUREMENT", 
	description = f"Extra measurement of '{name}' was deleted ")
	return HttpResponse('Deleted Successfully!!!')

@login_required	
@api_view(['GET'])
def show_extra_measurement(request):	
	measurement_id = request.GET.get("measurement_id")
	measurement = get_object_or_404(Measurement,id=measurement_id, customer__tailor=request.user)
	extra_measurement = measurement.extrameasurement_set.all()
	data = render_to_string("tailor_app/show_extra_measurement.html", {"extra_measurement" : extra_measurement}) 
	return HttpResponse(data)

@login_required	
@api_view(['GET'])
def edit_form_measurement(request):
	measurement_id = request.GET.get("measurement_id")
	measurement = get_object_or_404( Measurement, customer__tailor = request.user, id=measurement_id)
	id = measurement.id
	measurement_form = MeasurementForm2(instance = measurement )
	data = render_to_string("tailor_app/update_measurement_data.html", {"measurement_form" : measurement_form, "id":id}, request=request) 
	return HttpResponse(data)


@login_required	
@api_view(['POST'])
def edit_measurement(request):	
	instance = get_object_or_404(Measurement,id = request.POST.get("id"))
	measurement = MeasurementForm2(request.POST, instance=instance).save(commit=False)
	measurement.save()
	request.user.report_set.create(status = "EDIT-MEASUREMENT", 
	description = f"Measurement by '{measurement.customer}' was edited ")
	return HttpResponse('Success')


############################ REPORTS ###########################################


@login_required
def reports_page(request):
	user = request.user
	all_reports=  Report.objects.filter(tailor = user).order_by("-created_on")
	page = request.GET.get('page', 1)
	paginator = Paginator(all_reports, 20)
	try:
		reports = paginator.page(page)
	except PageNotAnInteger:
		reports = paginator.page(1)
	except EmptyPage:
		reports = paginator.page(paginator.num_pages)
	context = {
    'reports': reports,
    }
	return render(request, 'tailor_app/reports.html', context)


############################ SETTINGS ###########################################


@login_required
def settings(request):
	user = request.user
	print(request.POST)
	if request.method == 'POST' and request.POST.get("type") == "profile":
		print("enterde")
		user_form = EditUserForm(request.POST, request.FILES, instance = user)
		change_password_form = PasswordChangeForm(user)
		if user_form.is_valid():
			user_form.save()
			request.user.report_set.create(status = "EDIT-PROFILE", 
	description = f"Your Profile was edited ")
			return redirect('tailor_app:settings')
	elif request.method == 'POST' and request.POST.get("type") == "password":
		user_form = EditUserForm( instance = user)
		change_password_form = PasswordChangeForm(user ,request.POST)
		if change_password_form.is_valid():
			user = change_password_form.save()
			request.user.report_set.create(status = "UPDATE-PASSWORD", 
	description = "You updated your password")
			update_session_auth_hash(request, user)
			messages.success(request, "Your Password has been Updated Succesfully")		
		else:
			messages.error(request, "Please Correct The Error Below")
	else:
		user_form = EditUserForm(instance =user)
		change_password_form = PasswordChangeForm(user)
	return render(request, 'tailor_app/settings.html',  {
		'user_form': user_form,
		"change_password_form": change_password_form
		} )

