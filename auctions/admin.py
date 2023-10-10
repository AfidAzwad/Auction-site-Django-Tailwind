from django.contrib import admin
from .models import AUCTION, BID


@admin.register(AUCTION)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'auction_start_date', 'auction_end_date', 'min_bid_amount', 'auction_winner')
    list_filter = ('product_id',)  # Add filters

@admin.register(BID)
class BidAdmin(admin.ModelAdmin):
    list_display = ('serial', 'product_id', 'bider_id', 'bid_amount', 'auction_id')
    list_filter = ('product_id', 'auction_id', 'bider_id') 
