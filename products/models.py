from django.db import models
from users.models import User
from django.utils import timezone


AUCTION_STATUS_CHOICES =(
    ("draft", "Draft"),
    ("confirm", "Confirmed"),
    ("ended", "Ended"),
)


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


class PRODUCT(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_description = models.TextField(max_length=250)
    product_category = models.ForeignKey(CATEGORY, on_delete=models.CASCADE, null=False)
    product_image = models.ImageField(upload_to='images/', blank=True)
    product_owner = models.ForeignKey(to=User, db_column="product owner", on_delete=models.CASCADE, default=True, null=False)
    created_at = models.DateTimeField(default=timezone.now)

    @staticmethod
    def get_all_products():
        return PRODUCT.objects.all().order_by('-product_id')

    def __str__(self):
        return str(self.product_id) + " " + self.product_name
