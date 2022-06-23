import json
from io import BytesIO
from PIL import Image
from django.core.files.base import File

from django.utils import timezone
from django.test import TestCase, Client
from django.urls import reverse
from account.models import User
from ..models import Customer, Measurement


class TestCustomerPage(TestCase):

    @staticmethod
    def get_image_file(name="test_view_image.png", ext="png", size=(50,50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color= color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    def setUp(self):
        self.client = Client()
        self.valid_customer_data = {'name': 'emmanuel',
        'email' : 'emma@gmail.com',
        'sex' : 'Male',
        'phone_no' : '07037374323',
        'address': 'makoko'}
        
        self.user1 = User.objects.create_user(username ='Muffin',
            first_name= "ayo",
            last_name= "adediji",
            email= 'odeyemi@info.com',
            password= 'crazyclown1234',
            image = "avatar.png")
        self.customer1 = self.user1.customer_set.create(name = 'emmanuel1',
        email = 'emma@gmail.com',
        sex = 'Male',
        phone_no = '07037374323',
        address = 'makoko')
        self.customer_url = reverse('tailor_app:customer')
        self.add_customer_url = reverse('tailor_app:add_customer')
        self.delete_customer_url = reverse('tailor_app:delete_customer')
        self.edit_customer_url = reverse('tailor_app:edit_customer')



    def test_customer_page_with_get_request_and_valid_user(self):
        self.client.login(username = self.user1.username, password = 'crazyclown1234')
        response = self.client.get(
            self.customer_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "customers")
        self.assertContains(response, "customer_form")
        self.assertTemplateUsed(response, "tailor_app/customers.html")  

    def test_customer_page_with_get_request_and_invalid_user(self):
        self.client.login(username = self.user1.username, password = 'crazyclown1231')
        response = self.client.get(
            self.customer_url,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('account:login')}?next={reverse('tailor_app:customer')}")

    def test_add_customer_page_with_valid_user_and_data(self):
        self.client.login(username = self.user1.username, password = 'crazyclown1234')
        response = self.client.post(
            self.add_customer_url,
            data = self.valid_customer_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user1.customer_set.count(), 2)

    def test_delete_customer_page_with_valid_user_and_data(self):
        self.client.login(username = self.user1.username, password = 'crazyclown1234')
        response = self.client.post(
            self.delete_customer_url,
            data = {"customer_id":1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user1.customer_set.count(), 0)
        
        
class TestOrderPage(TestCase):

    def setUp(self):
        self.client = Client()
        self.valid_data = {
            "delivery_date" : timezone.now().date(),
            "amount" : 1000,
            'quantity':1, 'paid': 10, 'description':'None'
            }
        
        self.user1 = User.objects.create_user(username ='Muffin',
            first_name= "ayo",
            last_name= "adediji",
            email= 'odeyemi@info.com',
            password= 'crazyclown1234',
            image = "avatar.png")

        self.customer1 = self.user1.customer_set.create(name = 'emmanuel1',
            email = 'emma@gmail.com',
            sex = 'Male',
            phone_no = '07037374323',
            address = 'makoko')
        self.order1  = self.customer1.order_set.create(delivery_date = "2021-3-1", amount = 1000)
        self.order_url = reverse('tailor_app:orders')
        self.add_order_url = reverse('tailor_app:add_order')
        self.delete_order_url = reverse('tailor_app:delete_order')
        self.edit_order_url = reverse('tailor_app:edit_order')



    def test_order_page_with_get_request_and_valid_user(self):
        self.client.login(username = self.user1.username, password = 'crazyclown1234')
        response = self.client.get(
            self.order_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tailor_app/orders.html") 

    # def test_add_order_page_with_valid_user_and_data(self):
    #     self.client.login(username = self.user1.username, password = 'crazyclown1234')
    #     response = self.client.post(
    #         self.add_order_url,
    #         data = self.valid_data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(self.user1.order_set.count(), 2) 


class TestMeasurePage(TestCase):

    def setUp(self):
        self.client = Client()
        self.valid_data = {'neck' : 10 ,
                        'waist' : 10,
                        'wrist' : 10 ,
                        'sleeve_length' : 10 ,
                        'chest' : 10,
                        'shoulder' : 10 ,
                        'thigh' : 10 ,
                        'ankle' : 10}
        
        self.user1 = User.objects.create_user(username ='Muffin',
            first_name= "ayo",
            last_name= "adediji",
            email= 'odeyemi@info.com',
            password= 'crazyclown1234',
            image = "avatar.png")
        self.customer1 = self.user1.customer_set.create(name = 'emmanuel1',
        email = 'emma@gmail.com',
        sex = 'Male',
        phone_no = '07037374323',
        address = 'makoko')
        self.measurement1 = Measurement.objects.create(customer=self.customer1, waist=10, neck = 10)
        self.extrameasurement1 = self.measurement1.extrameasurement_set.create(name="waist_line", value=100)
        self.measurement_url = reverse('tailor_app:measurements')
        self.add_measurement_url = reverse('tailor_app:add_measurement')
        self.delete_measurement_url = reverse('tailor_app:delete_measurement')
        self.edit_measurement_url = reverse('tailor_app:edit_measurement')

        self.add_extra_measurement_url = reverse('tailor_app:add_extra_measurement')
        self.delete_extra_measurement_url = reverse('tailor_app:delete_extra_measurement')



    def test_measurement_page_with_get_request_and_valid_user(self):
        self.client.login(username = self.user1.username, password = 'crazyclown1234')
        response = self.client.get(
            self.measurement_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tailor_app/measurement.html")  

    # def test_add_measurement_with_valid_user_and_data(self):
    #     self.client.login(username = self.user1.username, password = 'crazyclown1234')
    #     response = self.client.post(
    #         self.add_measurement_url,
    #         data = self.valid_data)
    #     self.assertEqual(response.status_code, 200)


class TestSettingsPage(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_customer_data = {'first_name': 'emmanuelNew',
        'email' : 'emma@gmail.com',
        'sex' : 'Male',
        'phone_no' : '07037374323',
        'address': 'makoko'}
        
        self.user1 = User.objects.create_user(username ='Muffin',
            first_name= "ayo",
            last_name= "adediji",
            email= 'odeyemi@info.com',
            password= 'crazyclown1234',
            image = "avatar.png")
        self.settings_url = reverse('tailor_app:settings')

    def test_settings_page_with_get_request_and_valid_user(self):
        self.client.login(username = self.user1.username, password = 'crazyclown1234')
        response = self.client.get(
            self.settings_url,
        )
        self.assertEqual(response.status_code, 200)
        
        self.assertTemplateUsed(response, "tailor_app/settings.html") 

    def test_user_update(self):
        self.client.login(username = self.user1.username, password = 'crazyclown1234')
        self.valid_customer_data.update({"type":"profile"})
        response = self.client.post(
            self.settings_url,
            data = self.valid_customer_data)
        self.assertRedirects(response, reverse('tailor_app:settings'))
        self.assertEquals(self.user1.first_name, "emmanuelNew")

    def test_user_password(self):
        self.client.login(username = self.user1.username, password = 'crazyclown1234')
        self.valid_customer_data.update({"type":"profile"})
        response = self.client.post(
            self.settings_url,
            data = self.valid_customer_data)
        self.assertRedirects(response, reverse('tailor_app:settings'))

