from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Category(models.Model):
    c_id = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=100)

    def __str__(self):
        return self.cname


class PRODUCTS(models.Model):
    p_id = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=50)
    p_des = models.TextField(max_length=250)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=True, null=False)
    p_photo = models.ImageField(upload_to='images/')
    endate = models.DateField()
    min_bid = models.IntegerField()
    owner = models.ForeignKey(
        to=User, db_column="owner", on_delete=models.CASCADE, default=True, null=False)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    winner = models.CharField(max_length=50, blank=True)

    @staticmethod
    def get_all_products():
        return PRODUCTS.objects.all().order_by('-p_id')

    def __str__(self):
        return str(self.p_id) + " " + self.pname


class BIDS(models.Model):
    serial = models.AutoField(primary_key=True)
    product = models.ForeignKey(
        PRODUCTS, db_column="product", on_delete=models.CASCADE, default=True, null=False)
    bider = models.ForeignKey(
        to=User, db_column="bider", on_delete=models.CASCADE, default=True, null=False)
    price = models.CharField(max_length=20)

    @staticmethod
    def get_all_products():
        return BIDS.objects.all().order_by('-serial')

    def __str__(self):
        return str(self.serial)
