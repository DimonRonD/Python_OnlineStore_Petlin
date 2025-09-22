from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Goods_category, Goods, Warehouse, Customers, Status, Orders, Order_status, Order_goods, Cart, Brand


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Goods_category)
admin.site.register(Goods)
admin.site.register(Warehouse)
admin.site.register(Customers)
admin.site.register(Status)
admin.site.register(Orders)
admin.site.register(Order_status)
admin.site.register(Order_goods)
admin.site.register(Cart)
admin.site.register(Brand)