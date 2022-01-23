from datetime import date
from django.shortcuts import render, redirect
from django.db import models
from .models import *
from . import forms
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib import auth


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
