from django.shortcuts import render,redirect
from django.contrib.auth.models import User
# Create your views here.
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required



@login_required(login_url='/login')
def home(request):
    return render(request,'home.html')

def login_attempt(request):
    print("entered in login")
    if request.method =='POST':
        username = request.POST.get('username')
        print("this is username",username)
        password=request.POST.get('password')
        print("this is password",password)
        user_obj=User.objects.filter(username=username).first()
        print("this is user_obj",user_obj)
        if user_obj is None:
            messages.success(request, 'user is not found')
            return redirect('/login')
        profile_obj =Profile.objects.filter(user= user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, 'your email is not verified ')
            return redirect('/login')
        user =authenticate(username=username,password=password)
        if user is None:
            messages.success(request, 'username or password is not correct ')
            return redirect('/login')
        login(request,user)
        return redirect('/')
    return render(request,'login.html')

def register_attempt(request):
    if request.method =='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            if User.objects.filter(username=username).first():
                messages.success(request,'Username is already taken')
                return redirect('/register')
            if User.objects.filter(email=email).first():
                messages.success(request, 'Email is already taken')
                return redirect('/register')
            # user_obj = User.objects.create_user(username=username,email=email,password=password)
            user_obj = User(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj=Profile.objects.create(user=user_obj,auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email,auth_token)
            messages.success(request, 'Veification link has been sent ! please check your mail')
            return redirect('/token')
        except Exception as e:
            print(e)


    return render(request,'register.html')
def verify (request,auth_token):
    try:
        print("entered in verify")
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'This account has already verified')
                return redirect("/success")
            profile_obj.is_verified=True
            profile_obj.save()
            messages.success(request, 'Congrats email has been verified successfully')
            return redirect("/success")
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
def send_mail_after_registration(email,token):
    subject='Your account need to be Verified'
    message= f'Hey please click the link http://127.0.0.1:8000/verify{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)

def send_mail_for_forget_password(email,token):
    subject='This is your forget password link please click and reset your password'
    message= f'Hey please click the link http://127.0.0.1:8000/check_forget_pass_token{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,email_from,recipient_list)

def error(request):
    return render(request,'error.html')

def success(request):
    return render(request,'success.html')
def token_send(request):
    return render(request,'token_send.html')



@login_required(login_url='/login')
def logout_task(request):
    logout(request)
    return redirect('login')


def forgotpassword(request):
    if request.method =='POST':
        print("this sis request tha the iuser has posted.",request.POST.get('email'))
        email= request.POST.get('email')
        get_user= User.objects.get(email=email)
        print("this is the request user _ id ",get_user.id)
        get_user_id=get_user.id
        get_user_auth_token=Profile.objects.get(user_id=get_user_id)
        now_extract_token_of_user= get_user_auth_token.auth_token
        print("this is the requested user auth token ",now_extract_token_of_user)
        send_mail_for_forget_password(email, now_extract_token_of_user)
        messages.success(request, 'Forgot password link has been sent ! please check your mail')
        return render(request,'forget_password.html')
    else:
        return render(request,'forget_password.html')


def check_forget_pass_token(request,auth_token):
    print("1")
    try:

        print("entered in check_forget_pass_token")
        profile_obj=Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                return redirect("/password_reset")
            else:
                messages.success(request, 'Please first verify your account')
                return redirect("/error")
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
def password_reset(request):
    if request.method =='POST':
        password = request.POST.get('password')
        print("this is new password",password)
        email = request.POST.get('email')
        print("this is user", email)
        get_user = User.objects.get(email=email)
        print("this is the user",get_user)
        get_user.set_password(password)
        get_user.save()
    return render(request,'password_reset.html')