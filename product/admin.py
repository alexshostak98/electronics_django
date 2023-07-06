from django.contrib import admin
from product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_type',
        'name',
        'model',
        'market_launch_date',
    )
    ordering = ['-market_launch_date']
