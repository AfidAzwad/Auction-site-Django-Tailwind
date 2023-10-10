from django.db import models
from users.models import User
from django.utils import timezone
from products.models import CATEGORY, PRODUCT


AUCTION_STATUS_CHOICES =(
    ("draft", "Draft"),
    ("confirm", "Confirmed"),
    ("ended", "Ended"),
)

class AUCTION(models.Model):
    product_id = models.ForeignKey(PRODUCT, db_column="product", on_delete=models.CASCADE, default=True, null=False)
    auction_start_date = models.DateTimeField(default=timezone.now)
    auction_created_by = models.ForeignKey(User, db_column="bider", on_delete=models.CASCADE, default=True, null=False)
    auction_end_date = models.DateField()
    min_bid_amount = models.IntegerField()
    status = models.CharField('Status', max_length=10, choices=AUCTION_STATUS_CHOICES)
    auction_winner = models.CharField(max_length=50, blank=True)


class BID(models.Model):
    serial = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(PRODUCT, db_column="product", on_delete=models.CASCADE, default=True, null=False)
    bider_id = models.ForeignKey(User, db_column="bider", on_delete=models.CASCADE, default=True, null=False)
    bid_amount = models.CharField(max_length=20)
    auction_id = models.ForeignKey(AUCTION, db_column="auction", on_delete=models.CASCADE, default=True, null=False)

    @staticmethod
    def get_all_products():
        return BID.objects.all().order_by('-serial')

    def __str__(self):
        return str(self.serial)
