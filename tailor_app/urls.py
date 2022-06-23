from django.urls import path
from . import views

app_name = 'tailor_app'

urlpatterns = [
    ################################## CUSTOMER URLS ########################################

    path('customers/all/', 
    views.customers_page, 
    name='customer'),

    path('customers/search/', 
    views.search_customers, 
    name='search_customer'),

    path('customers/add/', 
    views.add_customer, 
    name='add_customer'),

    path('customers/edit/', 
    views.edit_customer, 
    name='edit_customer'),

    path('customer/delete/', 
    views.delete_customer, 
    name='delete_customer'),

    path('customer/edit/form/',
    views.edit_form_customer,
    name='edit_form_customer'),
    
 ################################## ORDER URLS ########################################


    path('orders/all/', 
    views.orders_page,
    name='orders'),

    path('order/add/',
    views.add_order,
    name='add_order'),

    path('order/delete/',
    views.delete_order,
    name='delete_order'),

    path('order/edit/form/',
    views.edit_form_order,
    name='edit_form_order'),

    path('order/edit/',
    views.edit_order,
    name='edit_order'),

################################## MEASUREMENT URLS ########################################


    path('measurements/all/', 
    views.measurements_page, 
    name='measurements'),

    path('measurements/add/',
    views.add_measurement,
    name='add_measurement'),

    path('extra_measurements/add/',
    views.add_extra_measurement,
    name='add_extra_measurement'),

    path('measurement/delete/',
    views.delete_measurement,
    name='delete_measurement'),

    path('extra_measurement/delete/',
    views.delete_extra_measurement,
    name='delete_extra_measurement'),

    path('measurement/show_extra_measurement_table/',
    views.show_extra_measurement,
    name='show_extra_measurement_table'),

    path('measurement/edit/form/',
    views.edit_form_measurement,
    name='edit_form_measurement'),

    path('measurement/edit/',
    views.edit_measurement,
    name='edit_measurement'),

################################## REPORTS URLS ########################################



    path('reports/all/', 
    views.reports_page, 
    name='reports'),


    path('settings/', views.settings, name='settings'),
   
]
