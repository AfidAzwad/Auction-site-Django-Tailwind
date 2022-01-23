from django import forms
from django.contrib.auth.forms import User, UserCreationForm
from django.forms import fields
from django.forms.fields import NullBooleanField
from . import models
    
class SignupForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'type': 'text', 'placeholder': "first name"}), required=True, max_length=50, label='')
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'type': 'text', 'placeholder': "lastname"}), required=True, max_length=50, label='')
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'type': 'text', 'placeholder': "Enter username"}), required=True, max_length=50, label='')
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'type': 'email', 'placeholder': "email"}), required=True, max_length=50, label='')
    password1 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'type': 'password', 'placeholder': "password"}), required=True, max_length=50, label='')
    password2 = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'type': 'password', 'placeholder': "enter the same password as before, for verification"}), required=True, max_length=50, label='')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

