from django.db import models
from users.models import User
from datetime import datetime



class CATEGORY(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        # Converting category_name to lowercase before saving
        self.category_name = self.category_name.lower()
        super(CATEGORY, self).save(*args, **kwargs)
    
    @property
    def formatted_category_name(self):
        return self.category_name.title()


class PRODUCTS(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_description = models.TextField(max_length=250)
    product_category = models.ForeignKey(CATEGORY, on_delete=models.CASCADE, default=True, null=False)
    product_image = models.ImageField(upload_to='images/')
    product_owner = models.ForeignKey(to=User, db_column="product owner", on_delete=models.CASCADE, default=True, null=False)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    @staticmethod
    def get_all_products():
        return PRODUCTS.objects.all().order_by('-product_id')

    def __str__(self):
        return str(self.product_id) + " " + self.product_name


class AUCTIONS(models.Model):
    product_id = models.ForeignKey(PRODUCTS, db_column="product", on_delete=models.CASCADE, default=True, null=False)
    auction_start_date = models.DateTimeField(default=datetime.now, blank=True)
    auction_end_date = models.DateField()
    min_bid_amount = models.IntegerField()
    auction_winner = models.CharField(max_length=50, blank=True)


class BIDS(models.Model):
    serial = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(PRODUCTS, db_column="product", on_delete=models.CASCADE, default=True, null=False)
    bider_id = models.ForeignKey(User, db_column="bider", on_delete=models.CASCADE, default=True, null=False)
    bid_amount = models.CharField(max_length=20)
    auction_id = models.ForeignKey(AUCTIONS, db_column="auction", on_delete=models.CASCADE, default=True, null=False)

    @staticmethod
    def get_all_products():
        return BIDS.objects.all().order_by('-serial')

    def __str__(self):
        return str(self.serial)
