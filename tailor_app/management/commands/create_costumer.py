from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from account.models import User
from tailor_app.models import Customer

class Command(BaseCommand):
    help = 'Create customer'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of customers to be created')
        
  
        
    def handle(self, *args, **kwargs):
        total = kwargs['total']
        users = User.objects.all()
        for user in users:
            for num in range(1,total+1):
                user.customer_set.create(name = f'test user{num}',
                phone_no = num,
                email = "testcustomer@yahoo.com",
                sex = "Male",
                address = "Makoko")

        self.stdout.write(self.style.SUCCESS('customerS created with success!'))