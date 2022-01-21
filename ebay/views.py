from datetime import date
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import models
from .models import *
from . import forms
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import token_generator
from django.urls import reverse
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def signup(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        pwd1 = request.POST.get('password1')
        pwd2 = request.POST.get('password2')

        if len(pwd1) < 8:
            messages.add_message(request, messages.ERROR,
                                 'Password should be at least 6 characters')
        if pwd1 != pwd2:
            messages.add_message(request, messages.ERROR,
                                 'Password mismatch!!')
        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'Enter a valid email address')

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 'Username is taken, choose another one')
            diction = {'title': "Registration", 'signupform': form}
            return render(request, 'registration/Signup.html', context=diction)

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'Email is already taken !')
            diction = {'title': "Registration", 'signupform': form}
            return render(request, 'registration/Signup.html', context=diction)

        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
        else:
            messages.add_message(request, messages.ERROR,
                                 'password is not valid !!!')
            diction = {'title': "Registration", 'signupform': form}
            return render(request, 'registration/Signup.html', context=diction)

        #user = authenticate(username=username, password=pwd1)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
    
        link = reverse('activate', kwargs={
            'uidb64': uidb64, 'token': token_generator.make_token(user) })
        
        activate_url = 'http://'+domain+link

        email_body = 'Hi '+ user.username + \
        'Please use this link to verify your account\n' + activate_url

        email_subject = 'Activate your account'

        email = EmailMessage(
            email_subject, email_body,
            'noreply@semycolon.com',
            [email],
        )
        email.send(fail_silently=False)
        messages.success(request, 'Account successfully created')

        return redirect('login')

    diction = {'title': "Registration", 'signupform': form}
    return render(request, 'registration/Signup.html', context=diction)


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('ebay:home'))
        messages.error(
            request, 'Please fill all fields')
        return render(request, 'registration/login.html')


class LogoutView(View):
    def post(self, request):
        logout(request)
        #messages.success(request, 'You have been logged out')
        return redirect(reverse('ebay:home'))


# def login_user(request):
#     if request.method == 'POST':
#         context = {'data': request.POST}
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user and not user.email_verified:
#             messages.add_message(request, messages.ERROR,
#                                  'Email is not verified, please check your email inbox')
#             return render(request, 'registration/login.html', context, status=401)

#         if not user:
#             messages.add_message(request, messages.ERROR,
#                                  'Invalid credentials, try again')
#             return render(request, 'registration/login.html', context, status=401)

#         messages.add_message(request, messages.success,
#                                  'Account Created Successfully !')
#         login(request, user)
#         return redirect(reverse('ebay:home'))

#     return render(request, 'registration/login.html')


def home(request):
    # EMAIL= request.session['emailid']
    items = PRODUCTS.get_all_products()
    if request.GET:
        searched = request.GET['search']
        items = PRODUCTS.objects.filter(pname__contains=searched)

    diction = {'title': "Homepage", 'products': items}
    return render(request, 'ebay/home.html', context=diction)


def bidder(request):
    EMAIL = request.session['emailid']
    bidder = BIDS.get_all_products()
    diction = {'title': "Bidder Information",
               'bidders': bidder, 'email': EMAIL}
    return render(request, 'ebay/bidderinfo.html', context=diction)


def addproducts(request):
    EMAIL = request.session['emailid']
    form = forms.addproductForm()
    form.fields['owner'].initial = EMAIL
    form.fields['winner'].initial = "TBA"

    if request.method == "POST":
        form = forms.addproductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product Added')
            return redirect('ebay:addproduct')

    diction = {'title': "Add Product", 'addproductForm': form, 'email': EMAIL}
    return render(request, 'ebay/addproduct.html', context=diction)


def update(request, pid):
    EMAIL = request.session['emailid']
    productinfo = PRODUCTS.objects.get(p_id=pid)
    form = forms.addproductForm(instance=productinfo)

    if request.method == "POST":
        form = forms.addproductForm(request.POST, instance=productinfo)

        if form.is_valid():
            form.save(commit=True)
            return redirect('ebay:admindash')

    diction = {'title': "Product Update", 'productinfo': form, 'email': EMAIL}
    return render(request, 'ebay/productupdate.html', context=diction)


def deletion(request, pid):
    PRODUCTS.objects.get(p_id=pid).delete()
    return redirect('ebay:admindash')
