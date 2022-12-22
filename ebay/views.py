from django.db.models import Q
from datetime import date
import pandas as pd
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


def productstatus():
    Products = PRODUCTS.objects.all()
    ID = Products.values_list('p_id', flat=True)
    today = date.today()

    for pid in ID:
        p = PRODUCTS.objects.get(p_id=pid)
        if BIDS.objects.filter(Q(product=pid), Q(product__endate__lte=today)).exists():
            highest = BIDS.objects.filter(
                product=pid).order_by('-price').first()
            PRODUCTS.objects.filter(p_id=pid).update(
                winner=highest.bider.email)
            win = True

        if PRODUCTS.objects.filter(Q(p_id=pid), Q(endate__lte=today)).exists() and not BIDS.objects.filter(product=pid).exists():
            PRODUCTS.objects.filter(p_id=pid).update(
                winner="No bid")


def home(request):
    productstatus()
    category = request.GET.get('category')
    categories = Category.objects.all()

    if category != None:
        items = PRODUCTS.objects.filter(category__cname=category)
    else:
        items = PRODUCTS.get_all_products()[:6]

    diction = {'title': "Homepage", 'products': items,
               'categories': categories, }
    return render(request, 'ebay/home.html', diction)


def allproduct(request):
    query = ""
    diction = {}
    category = request.GET.get('category')
    categories = Category.objects.all()

    if category != None:
        items = PRODUCTS.objects.filter(category__cname=category)
    elif 'search' in request.GET:
        query = request.GET.get('search')
        items = PRODUCTS.objects.filter(pname__icontains=query)
    else:
        items = PRODUCTS.get_all_products()

    paginator = Paginator(items, 6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    diction = {'title': "All Products", 'products': items,
               'categories': categories, 'page_obj': page_obj, 'query': query}
    return render(request, 'ebay/allproduct.html', diction)


@login_required(login_url='/accounts/login')
def addproducts(request):
    form = forms.addproductForm()
    today = date.today()
    if request.method == "POST":
        enddate = request.POST['endate']
        price = int(request.POST['min_bid'])
        enddate = pd.to_datetime(enddate).date()
        form = forms.addproductForm(request.POST, request.FILES)
        if form.is_valid():
            if enddate <= today:
                messages.error(request, 'Auction End-Date is not valid !')
                return redirect('ebay:addproduct')
            elif price < 0:
                messages.error(request, 'Price cant be negative !')
                return redirect('ebay:addproduct')
            else:
                instance = form.save(commit=False)
                instance.winner = "TBA"
                instance.owner = request.user
                instance.save()
                messages.success(request, 'Product Added')
                return redirect('ebay:addproduct')

    diction = {'title': "Add Product", 'addproductForm': form}
    return render(request, 'ebay/addproduct.html', context=diction)


@login_required(login_url='/accounts/login')
def myproduct(request):
    query = ""
    productstatus()
    if 'search' in request.GET:
        query = request.GET.get('search')
        items = PRODUCTS.objects.filter(
            Q(pname__icontains=query), Q(owner=request.user.id))
    else:
        items = PRODUCTS.objects.filter(owner=request.user).order_by('-p_id')

    paginator = Paginator(items, 6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    diction = {'title': "My products", 'products': items,
               'page_obj': page_obj, 'query': query}
    return render(request, 'ebay/myproducts.html', context=diction)


@login_required(login_url='/accounts/login')
def update(request, pid):
    today = date.today()
    p = PRODUCTS.objects.get(p_id=pid)

    if BIDS.objects.filter(Q(product=pid), Q(product__endate=today)).exists():
        highest = BIDS.objects.filter(
            product=pid).order_by('-price').first()
        PRODUCTS.objects.filter(p_id=pid).update(
            winner=highest.bider.email)
        messages.success(request, 'Winner is already found !')
        return redirect('ebay:myproduct')

    productinfo = PRODUCTS.objects.get(p_id=pid)
    form = forms.addproductForm(instance=productinfo)

    if request.method == "POST":
        enddate = request.POST['endate']
        price = int(request.POST['min_bid'])
        enddate = pd.to_datetime(enddate).date()
        form = forms.addproductForm(
            request.POST, request.FILES, instance=productinfo)

        if form.is_valid():
            if enddate <= today:
                messages.error(request, 'Auction End-Date is not valid !')
                diction = {'title': "Product Update", 'productinfo': form, }
                return render(request, 'ebay/productupdate.html', context=diction)
            elif price < 0:
                messages.error(request, 'Price cant be negative !')
                diction = {'title': "Product Update", 'productinfo': form, }
                return render(request, 'ebay/productupdate.html', context=diction)
            form.save(commit=True)
            messages.success(request, 'Product Updated Successfully !')
            return redirect('ebay:myproduct')

    diction = {'title': "Product Update", 'productinfo': form}
    return render(request, 'ebay/productupdate.html', context=diction)


@login_required(login_url='/accounts/login')
def deletion(request, pid):
    today = date.today()
    if BIDS.objects.filter(Q(product=pid), Q(product__endate=today)).exists():
        highest = BIDS.objects.filter(
            product=pid).order_by('-price').first()
        PRODUCTS.objects.filter(p_id=pid).update(
            winner=highest.bider.email)
        messages.success(request, 'Winner is already found !')
        return redirect('ebay:myproduct')

    PRODUCTS.objects.get(p_id=pid).delete()
    messages.error(request, 'Product Deleted Successfully !')
    return redirect('ebay:myproduct')


@login_required(login_url='/accounts/login')
def mybids(request):
    productstatus()
    query = ""
    diction = {}
    today = date.today()
    if 'search' in request.GET:
        query = request.GET.get('search')
        bids = BIDS.objects.filter(
            Q(product__pname__icontains=query) | Q(serial__icontains=query), Q(bider=request.user.id))
    else:
        bids = BIDS.objects.filter(bider=request.user.id).order_by('-serial')

    paginator = Paginator(bids, 6)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)

    diction = {'title': "My bids", 'bids': bids,
               'page_obj': page_obj, 'today': today, 'query': query}
    return render(request, 'ebay/mybids.html', context=diction)


@login_required(login_url='/accounts/login')
def biddelete(request, serial):
    BIDS.objects.get(serial=serial).delete()
    messages.error(request, 'Bid Deleted Successfully !')
    return redirect('ebay:mybids')


def productinfo(request, pid):
    win = False
    today = date.today()
    p = PRODUCTS.objects.get(p_id=pid)
    if BIDS.objects.filter(Q(product=pid), Q(product__endate__lte=today)).exists():
        highest = BIDS.objects.filter(
            product=pid).order_by('-price').first()
        PRODUCTS.objects.filter(p_id=pid).update(
            winner=highest.bider.email)
        win = True

    if PRODUCTS.objects.filter(Q(p_id=pid), Q(endate__lte=today)).exists() and not BIDS.objects.filter(product=pid).exists():
        PRODUCTS.objects.filter(p_id=pid).update(
            winner="No bid")

    bider = BIDS.objects.filter(product=pid).order_by('-serial')

    if request.user.is_authenticated:
        ownercheck = PRODUCTS.objects.filter(
            owner=request.user, p_id=p.p_id).exists()
        if request.method == "POST":
            price = int(request.POST["bidprice"])
            if price < 0:
                messages.error(
                    request, 'negative value is not accepted!!!')
            elif price < p.min_bid:
                messages.error(
                    request, 'bidding price cant be lower than minimum!!!')
            elif BIDS.objects.filter(product=pid, bider=request.user).exists():
                BIDS.objects.filter(bider=request.user,
                                    product=pid).update(price=price)
                messages.success(request, 'Bid Updated!!!')
            else:
                bid = BIDS(product=p, bider=request.user, price=price)
                bid.save()
                messages.success(request, 'Bid Submitted!!!')
            diction = {'title': "Product Info", 'products': p,
                       'bids': bider, 'win': win, 'today': today}
            return render(request, 'ebay/productinfo.html', context=diction)
        diction = {'title': "Product Info", 'products': p, 'bids': bider,
                   'win': win, 'ownercheck': ownercheck, 'today': today}
        return render(request, 'ebay/productinfo.html', context=diction)

    diction = {'title': "Product Info", 'products': p,
               'bids': bider, 'win': win, 'today': today}
    return render(request, 'ebay/productinfo.html', context=diction)
