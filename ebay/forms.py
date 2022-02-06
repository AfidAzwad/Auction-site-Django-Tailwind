from django import forms
from django.contrib.auth.forms import User
from django.forms import fields
from django.forms.fields import NullBooleanField
from . import models


class addproductForm(forms.ModelForm):
    pname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'placeholder': "Enter product name"}), label='')
    p_des = forms.CharField(widget=forms.Textarea(attrs={
                            'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'placeholder': "Enter product description"}), label='')
    category = forms.Select(attrs={'class': 'form-control'})
    p_photo = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline'}), label='')
    endate = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'type': 'date'}), label='')
    min_bid = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'shadow w-full py-2 px-3 bg-body rounded focus:outline-none focus:shadow-outline', 'value': "$"}), label='')

    class Meta:
        model = models.PRODUCTS
        fields = ['pname', 'p_des', 'category', 'p_photo', 'endate', 'min_bid']
