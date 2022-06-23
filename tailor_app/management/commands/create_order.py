from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from account.models import User
from tailor_app.models import Costumer

class Command(BaseCommand):
    help = 'Create Order'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of orders to be created')
        
  
        
    def handle(self, *args, **kwargs):
        total = kwargs['total']
        costumers = Costumer.objects.all()
        for costumer in costumers:
            for num in range(1,total+1):
                costumer.order_set.create(delivery_date = "2021-1-10",
    amount =200,
    description = "Test description")

        self.stdout.write(self.style.SUCCESS('ORDER created with success!'))