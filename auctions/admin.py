from django.contrib import admin
from .models import PRODUCTS, CATEGORY, AUCTIONS, BIDS

@admin.register(PRODUCTS)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_category', 'product_owner')  # Customize the fields displayed in the list view

@admin.register(CATEGORY)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)

@admin.register(AUCTIONS)
class AuctionAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'auction_start_date', 'auction_end_date', 'min_bid_amount', 'auction_winner')
    list_filter = ('product_id',)  # Add filters

@admin.register(BIDS)
class BidAdmin(admin.ModelAdmin):
    list_display = ('serial', 'product_id', 'bider_id', 'bid_amount', 'auction_id')
    list_filter = ('product_id', 'auction_id', 'bider_id') 
