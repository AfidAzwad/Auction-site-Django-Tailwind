from django.db import models

class Admin(models.Model):
    a_id = models.AutoField(primary_key=True)
    aname = models.CharField(max_length=50)
    a_email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)


    def __str__(self):
        return self.aname

# Create your models here.
class CUSTOMER(models.Model):
    c_id = models.AutoField(primary_key=True)
    cname = models.CharField(max_length=50)
    c_email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.c_id)+ " " +self.c_email


class PRODUCTS(models.Model):
    p_id = models.AutoField(primary_key=True)
    pname = models.CharField(max_length=50)
    p_des = models.TextField(max_length=250)
    p_photo = models.ImageField(upload_to = 'images/')
    endate = models.DateField()
    min_bid = models.CharField(max_length=20)
    owner = models.EmailField(max_length=50)
    winner = models.CharField(max_length=50, blank=True)
      
    @staticmethod
    def get_all_products():
        return PRODUCTS.objects.all().order_by('-p_id')

    def __str__(self):
        return str(self.p_id)+ " " +self.pname


class BIDS(models.Model):
    Serial = models.AutoField(primary_key=True)
    pid = models.CharField(max_length=50)
    p_name = models.CharField(max_length=50)
    bider = models.EmailField(max_length=50)
    price = models.CharField(max_length=20)

    def __str__(self):
        return str(self.Serial)+ " " +str(self.pid)+ " " +self.p_name+ " " +self.bider