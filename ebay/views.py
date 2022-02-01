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
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def home(request):
    query = ""
    diction = {}

    if 'search' in request.GET:
        query = request.GET.get('search')
        diction['query'] = str(query).strip()
        items = PRODUCTS.objects.filter(pname__icontains=query)
        paginator = Paginator(items, 6)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        diction = {'title': "Homepage", 'products': items, 'page_obj': page_obj}
        return render(request, 'ebay/home.html', diction)
    else:
        items = PRODUCTS.get_all_products()

    paginator = Paginator(items,6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    diction = {'title': "Homepage", 'products': items, 'page_obj': page_obj}
    return render(request, 'ebay/home.html', diction)

@login_required(login_url='/account/login')
def addproducts(request):
    form = forms.addproductForm()
    if request.method == "POST":
        form = forms.addproductForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.winner = "TBA"
            instance.owner = request.user
            instance.save()
            messages.success(request, 'Product Added')
            return redirect('ebay:addproduct')

    diction = {'title': "Add Product", 'addproductForm': form}
    return render(request, 'ebay/addproduct.html', context=diction)


def myproduct(request):
    query = ""
    diction = {}

    if 'search' in request.GET:
        query = request.GET.get('search')
        diction['query'] = str(query).strip()
        items = PRODUCTS.objects.filter(pname__icontains=query) and PRODUCTS.objects.filter(owner=request.user)
        paginator = Paginator(items, 6)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator, page_number)
        diction = {'title': "Homepage", 'products': items, 'page_obj': page_obj}
        return render(request, 'ebay/myproducts.html', diction)
    else:
        items = PRODUCTS.objects.filter(owner=request.user)

    paginator = Paginator(items,6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    diction = {'title': "My products", 'products': items, 'page_obj': page_obj}
    return render(request, 'ebay/myproducts.html', context=diction)


def bidder(request):
    bidder = BIDS.get_all_products()
    diction = {'title': "Bidder Information",
               'bidders': bidder}
    return render(request, 'ebay/bidderinfo.html', context=diction)


def update(request, pid):
    productinfo = PRODUCTS.objects.get(p_id=pid)
    form = forms.addproductForm(instance=productinfo)

    if request.method == "POST":
        form = forms.addproductForm(request.POST, instance=productinfo)

        if form.is_valid():
            form.save(commit=True)
            messages.success(request,'Product Updated Successfully !')
            return redirect('ebay:myproduct')

    diction = {'title': "Product Update", 'productinfo': form}
    return render(request, 'ebay/productupdate.html', context=diction)


def deletion(request, pid):
    PRODUCTS.objects.get(p_id=pid).delete()
    messages.error(request,'Product Deleted Successfully !')
    return redirect('ebay:myproduct')


def productinfo(request,pid):
    win = False
    today = date.today()
    product = PRODUCTS.objects.get(p_id=pid)
    
    if BIDS.objects.filter(product=pid).exists():
        if PRODUCTS.objects.filter(p_id=pid,endate=today).exists():
          highest = BIDS.objects.filter(product=pid).order_by('-price').first()
          PRODUCTS.objects.filter(p_id=pid).update(winner = highest.bider)
          win = True
        else:
            breakpoint  
    bider = BIDS.objects.filter(product = pid).order_by('-serial')
    items = PRODUCTS.objects.get(p_id=pid)

    ownercheck = PRODUCTS.objects.filter(owner=request.user,p_id=items.p_id).exists()
    if request.method == "POST":
        price = request.POST["bidprice"]
        if price < items.min_bid:
            messages.error(request,'bidding price cant be lower than minimum!!!')
        elif BIDS.objects.filter(bider=request.user,product=items.pname).exists():
            BIDS.objects.filter(bider=request.user,product=items.pname).update(price=price)
            messages.success(request,'Bid Updated!!!')
        else:
            items = PRODUCTS.objects.get(p_id=pid)
            Input = BIDS.objects.create(product = items.pname , bider = request.user, price=price)
            Input.save()
            messages.success(request,'Bid Submitted!!!')

    diction = {'title' : "Product Info",'products' : items,'bids': bider, 'check' : ownercheck, 'win': win}
    return render(request,'ebay/productinfo.html', context= diction)