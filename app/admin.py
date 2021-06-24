from django.contrib import admin
from .models import *
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'product_code', 'quantity', 'selling_price', 'discount_price', 'brand', 'category']


admin.site.register(Product, ProductAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


admin.site.register(Cart, CartAdmin)


class OrderPlacedAdmin(admin.ModelAdmin):
    list_display=['id', 'user', 'customer', 'product', 'quantity', 'date_auto_now', 'date_auto_now_add']
admin.site.register(OrderPlaced, OrderPlacedAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'district', 'city']

admin.site.register(Customer, CustomerAdmin)


class MulyticAdmin(admin.ModelAdmin):
    list_display= ['id', 'customer_name', 'phone', 'email', 'order_time','product', 'quantity']

admin.site.register(Mulytic_labs_test, MulyticAdmin)

