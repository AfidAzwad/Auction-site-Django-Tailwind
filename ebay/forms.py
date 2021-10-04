from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.fields import NullBooleanField
from . import models


class adminLogin(forms.ModelForm):
    a_email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'placeholder': "email"}), label='')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'placeholder': "password"}), label='')

    class Meta:
        model = models.CUSTOMER
        fields = ('a_email', 'password')


class LoginForm(forms.ModelForm):
    c_email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'placeholder': "email"}), label='')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'placeholder': "password"}), label='')

    class Meta:
        model = models.CUSTOMER
        fields = ('c_email', 'password')


class SignUpForm(forms.ModelForm):
    cname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "name"}), label='')
    c_email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': "email"}), label='')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': "password"}), label='')

    class Meta:
        model = models.CUSTOMER
        fields = '__all__'


class addproductForm(forms.ModelForm):
    pname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Enter product name"}), label='')
    p_des = forms.CharField(widget=forms.Textarea(attrs={
                            'class': 'form-control', 'placeholder': "Enter product description"}), label='')
    p_photo = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control'}), label='')
    endate = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}), label='')
    min_bid = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'value': "$"}), label='')
    owner = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': "owner email"}), label='')
    winner = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "winner email"}), label='')

    class Meta:
        model = models.PRODUCTS
        fields = '__all__'
