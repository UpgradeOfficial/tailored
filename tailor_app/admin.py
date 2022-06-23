from django.contrib import admin
from .models import Order, Customer, Measurement, ExtraMeasurement,Report

# Register your models here.
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Measurement)
admin.site.register(ExtraMeasurement)
admin.site.register(Report)