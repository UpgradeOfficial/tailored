import json
from io import BytesIO
from PIL import Image
from django.core.files.base import File

from django.test import TestCase, Client
from django.urls import reverse
from ..models import User
from ..jwt_token import encoded_reset_token, decode_reset_token

# Create your tests here.

class TestSignUp(TestCase):

    @staticmethod
    def get_image_file(name="test_view_image.png", ext="png", size=(50,50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color= color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)


    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('account:signup')
        self.valid_payload = {
            'username': 'Muffin',
            'first_name': "ayo",
            'last_name': "adediji",
            'email': 'odeyemi@info.com',
            'password1': 'crazyclown1234',
            'password2': 'crazyclown1234',
            "image" : "avatar.png"
        }

    def test_create_user_with_valid_data(self):
        response = self.client.post(
            self.signup_url,
            data=self.valid_payload
        )
        self.assertRedirects(response, reverse('account:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.last().username, self.valid_payload['username'])

    def test_signup_with_get_request(self):
        response = self.client.get(
            self.signup_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")   



class TestLoginView(TestCase):


    def setUp(self):
        self.client = Client()
        self.login_url = reverse('account:login')
        self.user1 = User.objects.create_user(username ='Muffin',
            first_name= "ayo",
            last_name= "adediji",
            email= 'odeyemi@info.com',
            password= 'crazyclown1234',
            image = "avatar.png")

        self.valid_payload = {
            'username': 'Muffin',
            'password': 'crazyclown1234',
        }



    def test_login_with_valid_data(self):
        response = self.client.post(
            self.login_url,
            data=self.valid_payload
        )
        self.assertRedirects(response, reverse('account:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.last().username, self.valid_payload['username'])
    
    def test_login_with_invalid_data(self):
        self.valid_payload['username'] = "falseUsername"
        response = self.client.post(
            self.login_url,
            data=self.valid_payload
        )
        self.assertRedirects(response, reverse('account:home'))
        self.assertEqual(response.status_code, 302)

    def test_login_with_get_request(self):
        response = self.client.get(
            self.login_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/login.html")  


class TestDashboardView(TestCase):


    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username ='Muffin',
            first_name= "ayo",
            last_name= "adediji",
            email= 'odeyemi@info.com',
            password= 'crazyclown1234',
            image = "avatar.png")
        self.dashboard_url = reverse('account:dashboard')



    def test_dashboard_with_get_request(self):
        self.client.login(username = self.user1.username, password = 'crazyclown1234')
        response = self.client.get(
            self.dashboard_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/dashboard.html")  


class TestOtherView(TestCase):


    def setUp(self):
        self.client = Client()
        self.faq_url = reverse('account:faq')
        self.about_url = reverse('account:about')
        self.contact_url = reverse('account:contact')
        


    def test_faq_with_get_request(self):
        response = self.client.get(
            self.faq_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/faq.html")  

    def test_about_with_get_request(self):
        response = self.client.get(
            self.about_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/about.html")

    def test_contact_with_get_request(self):
        response = self.client.get(
            self.contact_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/contact.html")




class TestForgotView(TestCase):


    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username ='Muffin',
            first_name= "ayo",
            last_name= "adediji",
            email= 'odeyemi@info.com',
            password= 'crazyclown1234',
            image = "avatar.png")
        self.token = encoded_reset_token(self.user1.id)
        self.forgot_password_url = reverse('account:forgot_password')
        self.confirm_password_reset_url = reverse('account:confirm_password_reset', kwargs={"token": self.token})
        self.valid_token_and_password_payload = {
            'new_password1': 'crazyPassword',
            'new_password2': 'crazyPassword',
             }


    def test_forgot_password_with_get_request(self):
        response = self.client.get(
            self.forgot_password_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/forgot_password.html") 

    def test_password_token_with_get_request(self):
        response = self.client.get(
            self.confirm_password_reset_url,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/confirm_password_reset.html") 

    def test_password_token_with_post_request(self):
        response = self.client.post(
            self.confirm_password_reset_url,
            data = self.valid_token_and_password_payload
        )
        self.assertRedirects(response, reverse('account:login'))
        self.user1.refresh_from_db()
        self.assertTrue(self.user1.check_password(self.valid_token_and_password_payload['new_password1']))
        


    
