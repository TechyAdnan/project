
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login


# Create your views here.

def home(request):
    return render(request , 'home.html')

def login_attempt(request):
    return render(request , 'login.html')

def register_attempt(request):

    if request.method == 'post':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:

            if User.objects.filter(username = username).first():
                messages.success(request , 'Username is taken.')
                return redirect('/login')

            if User.objects.filter(email = email).first():
                messages.success(request , 'email is taken.')
                return redirect('/login')   
            
            user_obj = User.objects.create(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            
            profile_obj = profile.objects.create(user = user_obj , auth_token = auth_token )
            profile_obj.save()
            send_mail(email , auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)

        


    return render(request , 'register.html')


def success(request):
    return render(request , 'success.html')

def token_send(request):
    return render(request , 'token_send.html')

    


def send_mail(email , token):
    subject = 'your account need to be verified'
    message = 'hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    # email_from = settings.EMAIL.HOST.USER
    email_from = 'rokoci7471@wireps.com'
    recipient_list = ['rokoci7471@wireps.com']
    send_mail(subject, message, email_from, recipient_list)
    




