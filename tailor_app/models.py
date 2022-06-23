from django.db import models
from account.models import User
import string
from django.utils.crypto import get_random_string
from django.utils import timezone
import random








     
 
class Customer(models.Model):
    sex_choices = (('Male', 'Male'),('Female', 'Female'))
    tailor = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=20)
    email = models.EmailField()
    sex = models.CharField(max_length=10, choices = sex_choices)
    address = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add =True)
    updated_on = models.DateTimeField(auto_now =True)
    
    def __str__(self):
        return f'{self.name}'
    
    
class Order(models.Model):
    status_choices = (('Confirmed', 'Confirmed'),
    ('Processing', 'Processing'),
    ('Ready', 'Ready'),
    ('Delivered', 'Delivered'))
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    delivery_date = models.DateField()
    quantity = models.PositiveIntegerField(default = 1)
    amount = models.PositiveIntegerField()
    paid = models.PositiveIntegerField(default= 0)
    description = models.TextField()
    tracking_id = models.CharField(max_length=20, unique=True)
    status =  models.CharField(max_length=100, choices= status_choices, default= "Confirmed")
    created_on = models.DateTimeField(auto_now_add =True)
    updated_on = models.DateTimeField(auto_now =True)

    def __str__(self):
        return f'{self.status}'

    def days_remaining(self):
        return self.delivery_date - timezone.now().date()

    def save(self, *args, **kwargs):
        if  not self.tracking_id:
            while True:
                id = get_random_string()
                if not Order.objects.filter(tracking_id = id).exists():
                    break
            self.tracking_id = id
        super(Order, self).save(*args, **kwargs)
        
    
  
class Measurement(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    neck =  models.DecimalField(max_digits=11, decimal_places=3, default=0)
    waist =  models.DecimalField(max_digits=11, decimal_places=3, default=0)
    wrist =  models.DecimalField(max_digits=11, decimal_places=3, default=0)
    sleeve_length =  models.DecimalField(max_digits=11, decimal_places=3, default=0)
    chest =  models.DecimalField(max_digits=11, decimal_places=3, default=0)
    shoulder =  models.DecimalField(max_digits=11, decimal_places=3, default=0)
    thigh =  models.DecimalField(max_digits=11, decimal_places=3, default=0)
    ankle =  models.DecimalField(max_digits=11, decimal_places=3, default=0)

    def __str__(self):
        return f'{self.customer}'

class ExtraMeasurement(models.Model):
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE)
    name =  models.CharField(max_length=30)
    value =  models.DecimalField(max_digits=11, decimal_places=3) 
    created_on = models.DateTimeField(auto_now_add =True)
    updated_on = models.DateTimeField(auto_now =True)

    def __str__(self):
        return f'{self.measurement.customer} extra measurement'


class Report(models.Model):
    tailor =   models.ForeignKey(User, on_delete = models.CASCADE)
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add =True)
    updated_on = models.DateTimeField(auto_now =True)

    def __str__(self):
        return f'{self.tailor} report on {self.status}'