from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant', 'price', 'stock')
    list_filter = ('tenant',)
    search_fields = ('name', 'description')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'customer', 'product', 'quantity', 'status')
    list_filter = ('tenant', 'status')
    search_fields = ('customer__username', 'product__name')