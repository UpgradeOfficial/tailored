from .base import *

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = ['tailored4u.pythonanywhere.com']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'tailored4u$default',
       'USER' : 'tailored4u',
       'PASSWORD' : 'philip1234',
       'OPTIONS' : {
           'init_command' : "SET sql_mode ='STRICT_TRANS_TABLES'",
           },
       'HOST' : 'tailored4u.mysql.pythonanywhere-services.com',
   },
}



## WSGI ####

# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys
#
## assuming your django settings file is at '/home/tailored4u/mysite/mysite/settings.py'
## and your manage.py is is at '/home/tailored4u/mysite/manage.py'
path = '/home/tailored4u/tailored/'
if path not in sys.path:
    sys.path.append(path)
#
os.environ['DJANGO_SETTINGS_MODULE'] = 'tailored.settings.production'
#
## then:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


