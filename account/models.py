from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    #USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password','first_name','last_name','email']

    email_confirmed = models.BooleanField(default = False)
    image = models.ImageField(upload_to = "tailor/%Y/%m/%d/", default="avatar.png")

class ContactUs(models.Model):
    name = models.CharField(max_length=30, unique=True)
    email = models.EmailField()
    message = models.TextField()
    completed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add =True)
    updated_on = models.DateTimeField(auto_now =True)
    

    

    class Meta:
        verbose_name = _("")
        verbose_name_plural = _("s")

    def __str__(self):
        return self.name

    

    