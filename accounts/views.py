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
import threading
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import requests
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import re

specialCharacters = ['$', '#', '@', '!', '*']


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


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
        if len(pwd1) < 6:
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

            EmailThread(email).start()
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
                messages.error(request, 'Account already activated !')
                return redirect('login')

            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully !')
            return redirect('login')

        except Exception as ex:
            return render(request, 'registration/activate-failed.html')

        return redirect('login')


class LogoutView(View):
    def post(self, request):
        logout(request)
        return redirect(reverse('/'))


class RequestPasswordReset(View):
    def get(self, request):
        return render(request, 'registration/reset-password.html')

    def post(self, request):
        email = request.POST['email']
        if not validate_email(email):
            messages.error(request, 'Please give a valid email !')
            return render(request, 'registration/reset-password.html')
        current_site = get_current_site(request)
        user = User.objects.filter(email=email)
        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }
            link = reverse('accounts:set-new-password', kwargs={
                'uidb64': email_contents['uid'], 'token': email_contents['token']})

            reset_url = 'http://'+current_site.domain+link

            email_body = 'Hi there,' \
                ' Please use this link to reset your password\n' + reset_url

            email_subject = 'Password reset Instruction'

            email = EmailMessage(
                email_subject, email_body,
                'noreply@semycolon.com',
                [email])

            EmailThread(email).start()
            messages.success(request, 'We have sent a email to reset password')
            return render(request, 'registration/reset-password.html')
        else:
            messages.error(
                request, 'No user exists with this email, Please provide a valid email !')
            return render(request, 'registration/reset-password.html')


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        return render(request, 'registration/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, 'Passwords doest not match !')
            return render(request, 'registration/set-new-password.html', context)
        if len(password) < 6:
            messages.error(request, 'Password should be at least 6 characters')
            return render(request, 'registration/set-new-password.html', context)
        elif re.search('[0-9]', password) is None:
            messages.error(
                request, 'Your password must have at least 1 number')
            return render(request, 'registration/set-new-password.html', context)
        elif re.search('[A-Z]', password) is None:
            messages.error(
                request, 'Your password must have at least 1 uppercase letter')
            return render(request, 'registration/set-new-password.html', context)
        elif not any(c in specialCharacters for c in password):
            messages.error(
                request, 'Your password must have at least 1 special character ($, #, @, !, *)')
            return render(request, 'registration/set-new-password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')

        except Exception as identifier:
            import pdb
            pdb.set_trace()
            messages.info(request, 'something went wrong, try again')
            return render(request, 'registration/set-new-password.html', context)
