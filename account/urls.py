from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('offline/', views.offline, name='offline'),
    path('confirm-password-reset/<token>/', views.confirm_password_reset, name='confirm_password_reset'),
     path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('', views.home, name='home'),
    path('sw.js', TemplateView.as_view(template_name = "account/sw.js", content_type = "application/javascript"), name='sw.js'),
    path('app.js', TemplateView.as_view(template_name = "account/app.js", content_type = "application/javascript"), name='app.js'),
    path('manifest.json', TemplateView.as_view(template_name = "account/manifest.json", content_type = "application/manifest"), name='manifest.json')

]
