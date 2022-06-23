from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image', 'password1', 'password2', )

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password1')
        email = validated_data.get('email')
        user = User.objects.create_user(username=username, password=password, email=email)
        return user


class EditUserForm( forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'image' )

    
