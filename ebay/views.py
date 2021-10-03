from datetime import date
from django.shortcuts import render, redirect
from django.db import models
from django.contrib import messages
from .models import *
from . import forms
# Create your views here.
from django.contrib.auth import authenticate, login


def homepage(request):
    # EMAIL= request.session['emailid']
    items = PRODUCTS.get_all_products()
    if request.GET:
        searched = request.GET['search']
        items = PRODUCTS.objects.filter(pname__contains=searched)

    diction = {'title': "Homepage", 'products': items}
    return render(request, 'ebay/home.html', context=diction)


def login(request):
    form = forms.LoginForm()
    # if request.method == "POST":
    #   form = forms.SignUpForm(request.POST)
    #   if form.is_valid():
    #         email_id = form.cleaned_data['c_email'];
    #         request.session['emailid'] = email_id;
    #         request.session.set_expiry(0)

    #         for i in CUSTOMER.objects.all():
    #             if i.c_email == email_id:
    #                 messages.success(request,'successfull login')
    #                 return customers(request)
    #         form.save(commit=True)
    #         messages.success(request,'Account created')
    #         return customers(request)

    diction = {'title': "Login", 'registerfomr': form}
    # diction = {'title' : "login"}
    return render(request, 'ebay/login.html', context=diction)


def adminlogin(request):
    form = forms.adminLogin()
    if request.method == "POST":
        form = forms.adminLogin(request.POST)
        if form.is_valid():
            email_id = form.cleaned_data['a_email']
            password = form.cleaned_data['password']

            # request.session['emailid'] = email_id
            # request.session.set_expiry(0)

            for i in Admin.objects.all():
                if i.a_email == email_id and i.password == password:
                    messages.success(request, 'successfull login')
                    return redirect('ebay:admindash')

    diction = {'title': "Admin Login", 'adminform': form}
    return render(request, 'ebay/adminlogin.html', context=diction)


def adminDash(request):
    items = PRODUCTS.get_all_products()

    # if request.GET:
    #     searched = request.GET['search']
    #     items = PRODUCTS.objects.filter(pname__contains=searched)
    diction = {'title': "Admin Dashboard", 'products': items}
    return render(request, 'ebay/admindash.html', context=diction)


def register(request):
    form = forms.SignUpForm()

    # if request.method == "POST":
    #   form = forms.SignUpForm(request.POST)
    #   if form.is_valid():
    #         mailid = form.cleaned_data['c_email'];
    #         request.session['emailid'] = mailid;
    #         request.session.set_expiry(0)
    #         for i in CUSTOMER.objects.all():
    #              if i.c_email == mailid:
    #                  messages.success(request,'Account already existed!!!')
    #                  return customers(request)
    #         form.save(commit=True)
    #         messages.success(request, 'Account created')
    #         return customers(request)

    diction = {'title': "Registration", 'registerform': form}
    return render(request, 'ebay/signup.html', context=diction)


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

def update(request,pid):
    EMAIL = request.session['emailid']
    productinfo = PRODUCTS.objects.get(p_id=pid)
    form = forms.addproductForm(instance= productinfo)

    if request.method == "POST":
         form = forms.addproductForm(request.POST, instance=productinfo)

         if form.is_valid():
             form.save(commit=True)
             return redirect('ebay:admindash')

    diction = {'title':"Product Update", 'productinfo': form, 'email': EMAIL}
    return render(request, 'ebay/productupdate.html', context=diction)


def deletion(request, pid):
    PRODUCTS.objects.get(p_id=pid).delete()
    return redirect('ebay:admindash')
