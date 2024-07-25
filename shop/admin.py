from django.contrib import admin

from shop.models import Category, Product, Order, Characteristic, Brand, ProductCharacteristic

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Characteristic)
admin.site.register(Brand)
admin.site.register(ProductCharacteristic)
