from django.db import models
from django.contrib.auth.models import User
# class CUSTOMER(models.Model):
#     c_id = models.AutoField(primary_key=True)
#     cname = models.CharField(max_length=50)
#     c_email = models.EmailField(max_length=50)
#     password = models.CharField(max_length=50)

#     def __str__(self):
#         return str(self.c_id) + " " + self.c_email


class PRODUCTS(models.Model):
    p_id = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=50)
    p_des = models.TextField(max_length=250)
    p_photo = models.ImageField(upload_to='images/')
    endate = models.DateField()
    min_bid = models.CharField(max_length=20)
    owner = models.ForeignKey(to=User, db_column="owner", on_delete=models.CASCADE)
    winner = models.CharField(max_length=50, blank=True)

    @staticmethod
    def get_all_products():
        return PRODUCTS.objects.all().order_by('-p_id')

    def __str__(self):
        return str(self.p_id) + " " + self.pname


class BIDS(models.Model):
    serial = models.AutoField(primary_key=True)
    product = models.ForeignKey(PRODUCTS, db_column="product", on_delete=models.CASCADE)
    # p_name = models.ForeignKey(PRODUCTS, on_delete=models.CASCADE)
    bider = models.ForeignKey(to=User,db_column="bider", on_delete=models.CASCADE)
    price = models.CharField(max_length=20)

    @staticmethod
    def get_all_products():
        return BIDS.objects.all().order_by('-Serial')

    def __str__(self):
        return str(self.serial) + " " + self.bider