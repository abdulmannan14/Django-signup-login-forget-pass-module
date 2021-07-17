from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [

    path('', home,name='home'),
    path('login', login_attempt,name='login'),
    path('register', register_attempt,name='register'),
    path('token', token_send,name='token'),
    path('success', success,name='success'),
    path('verify<auth_token>', verify,name='verify'),
    path('check_forget_pass_token<auth_token>', check_forget_pass_token,name='check_forget_pass_token'),
    path('error', error,name='error'),
    path('logout/', logout_task,name='logout'),
    path('fogotpassword/', forgotpassword,name='forgetpassword'),
    path('password_reset/', password_reset,name='password_reset'),

]