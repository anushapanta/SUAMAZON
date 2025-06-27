from django.contrib import admin
from .models import *    
    # here every models is registered
admin.site.register([Admin, Customer, Category, Cart, Product,CartProduct, Order])










