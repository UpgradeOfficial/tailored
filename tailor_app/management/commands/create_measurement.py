from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from account.models import User
from tailor_app.models import Customer, Measurement

class Command(BaseCommand):
    help = 'Create Measurement'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of Measurements to be created')
        
  
        
    def handle(self, *args, **kwargs):
        total = kwargs['total']
        customers = Customer.objects.all()
        for customer in customers:
            for num in range(1,total+1):
                Measurement.objects.create(customer = customer,neck =  10,
    waist =  10,
    wrist =  10,
    sleeve_length =  10,
    chest =  10,
    shoulder =  10,
    thigh =  10,
    ankle = 10)

        self.stdout.write(self.style.SUCCESS('MEASUREMENT created with success!'))