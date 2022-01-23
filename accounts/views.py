from datetime import date
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import models
from .models import *
from . import forms
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.views import View
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
from django.contrib import auth


class RegistrationView(View):
    def get(self, request):
        form = forms.SignupForm()
        diction = {'title': "Registration", 'signupform': form}
        return render(request, 'registration/Signup.html', context=diction)

    def post(self, request):
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
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('accounts:activate', kwargs={
                           'uidb64': uidb64, 'token': token_generator.make_token(user)})
            activate_url = 'http://'+domain+link
            email_body = 'Hi ' + user.username + \
                ' Please use this link to verify your account\n' + activate_url

            email_subject = 'Activate your account'

            email = EmailMessage(
                email_subject, email_body,
                'noreply@semycolon.com',
                [email],)

            email.send(fail_silently=False)
            messages.success(request, 'Please check your email to activate !')
            return redirect('login')

        else:
            messages.add_message(request, messages.ERROR,
                                 'password is not valid !!!')
            diction = {'title': "Registration", 'signupform': form}
            return render(request, 'registration/Signup.html', context=diction)

        diction = {'title': "Registration", 'signupform': form}
        return render(request, 'registration/Signup.html', context=diction)


class LoginView(View):
    def get(self, request):
        return redirect('login')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                    return redirect(reverse('ebay:home'))
                messages.error(
                    request, 'Account is not active,please check your email')
                return redirect('login')
            messages.error(
                request, 'Invalid credentials,try again')
            return redirect('login')
        else:
            messages.error(
                request, 'Please fill all fields')
            return redirect('login')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                messages.success(request, 'Account already activated !')
                return redirect('login')

            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully !')
            return redirect('login')

        except Exception as ex:
            return render(request, 'authentication/activate-failed.html')

        return redirect('login')


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect(reverse('/'))
