from django.contrib import admin
from .models import PRODUCT, CATEGORY

@admin.register(PRODUCT)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_category', 'product_owner')  # Customize the fields displayed in the list view

@admin.register(CATEGORY)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
