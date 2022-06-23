from django.shortcuts import ( render,
    redirect,
    HttpResponse,
    get_object_or_404 )
from django.utils import timezone
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from .jwt_token import encoded_reset_token, decode_reset_token
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse

from .forms import SignUpForm
from tailor_app.models import Order, Report
from .models import ContactUs, User


# Create your views here.



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():            
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('account:dashboard')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user)
            return redirect('account:dashboard')
        else:
            return redirect('account:home')
    return render(request, 'account/login.html')
    
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('account:login')

@login_required        
def dashboard(request):
    num_of_orders = Order.objects.filter(customer__tailor = request.user).count()
    num_of_pending_orders = Order.objects.filter(customer__tailor = request.user, status = "confirmed").count()
    num_of_reports = Report.objects.filter(tailor = request.user, created_on__date = timezone.now().date()).count()
    
    context = {
        "num_of_orders" : num_of_orders,
        "num_of_reports" : num_of_reports,
        "num_of_pending_orders":num_of_pending_orders,

    }
    return render(request, 'account/dashboard.html', context)
        
        
def home(request):
    if request.user.is_authenticated:
        return redirect("account:dashboard")
    return render(request, 'account/homepage.html')



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        form = ContactUs.objects.create(name=name, email=email, message=message)
        messages.success(request, f"Hello {name}, Your message has been sent to admin")	


    return render(request, 'account/contact.html')

def forgot_password(request):
    email = request.GET.get('email')
    user = User.objects.filter( email=email)
    if user.exists():
        user = user.first()
        email = email 
        subject = "Password Reset Request"
        password_reset_template_name = "account/password_reset_template.txt"
        token =  encoded_reset_token(user.id)
        email_context = {
            "email":user.email,
            "name": user.username, 
            'domain':'127.0.0.1:8000',
            'site_name': 'Tailored',
            'url' : reverse('account:confirm_password_reset', kwargs={'token' :token}),
            "user": user,
            'token': token,
            'protocol': 'http'}
        email = render_to_string(password_reset_template_name, email_context)
            
        try:
            send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid Header Found.')
        messages.success(request, "A link to the password reset would be sent to this email if it exists!!!")	


    return render(request, 'account/forgot_password.html')
        
def about(request):
    return render(request, 'account/about.html') 

def faq(request):
    return render(request, 'account/faq.html')

def offline(request):
    return render(request, 'account/fallback.html')



    
          
def confirm_password_reset(request, token):
    if request.method == "POST":
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        if token and len(new_password1) >= 8 and new_password1 == new_password2:
            user_id = decode_reset_token(token)
            user = get_object_or_404(User, id=user_id)
            user.set_password(new_password1)
            user.email_confirmed = True
            user.save()
            messages.success(request, f"Password Reset Successfull, Login now !!!")	
            return redirect('account:login')
        
    return render(request, 'account/confirm_password_reset.html')