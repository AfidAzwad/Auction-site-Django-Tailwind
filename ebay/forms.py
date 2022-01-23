from django import forms
from django.contrib.auth.forms import User
from django.forms import fields
from django.forms.fields import NullBooleanField
from . import models
    
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
