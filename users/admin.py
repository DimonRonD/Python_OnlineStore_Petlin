from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import GoodCategory, Good, Warehouse, Customer, Status, Order, OrderStatus, OrderGood, Cart, Brand


# Register your models here.
admin.site.register(GoodCategory)
admin.site.register(Good)
admin.site.register(Warehouse)
admin.site.register(Customer, UserAdmin)
admin.site.register(Status)
admin.site.register(Order)
admin.site.register(OrderStatus)
admin.site.register(OrderGood)
admin.site.register(Cart)
admin.site.register(Brand)