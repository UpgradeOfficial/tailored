import json

from django.test import TestCase, Client
from ..forms import OrderForm, OrderForm2

# Create your tests here.
class TestSignUp(TestCase):

    def setUp(self):
        self.client = Client()
        self.valid_payload = {'customer':1,
        'quantity':2,
        'amount':100,
        'paid':100,
        'delivery_date':'2022-1-1',
        'description':'test description'}

    def test_create_order_with_valid_data(self):
        response = OrderForm2(self.valid_payload)
        self.assertTrue(response.is_valid())
