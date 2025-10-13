from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Customer(AbstractUser):
    patronym_name = models.CharField(max_length=100, verbose_name='Отчество')
    address = models.TextField()
    phone = models.CharField(max_length=15, verbose_name='Номер телефона')

class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=100)
    def __str__(self):
        return self.brand_name

class GoodCategory(models.Model):
    goods_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    def __str__(self):
        return self.category_name


class Good(models.Model):
    goods_id = models.AutoField(primary_key=True)
    goods_name = models.CharField(max_length=255)
    goods_descr = models.TextField()
    goods_price = models.DecimalField(max_digits=12, decimal_places=2)
    goods_img = models.ImageField(upload_to='goods/')
    goods_category_id = models.ForeignKey(GoodCategory, on_delete=models.PROTECT, related_name='goods')
    brand_id = models.ForeignKey(Brand, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.brand_id.brand_name} {self.goods_name}"

class Warehouse(models.Model):
    warehouse_id = models.IntegerField(null=False)
    goods_id = models.ForeignKey(Good, on_delete=models.PROTECT)
    goods_cnt = models.IntegerField(null=False)
    def __str__(self):
        return f"{self.goods_id}: {self.goods_cnt}"

class Status(models.Model):
    order_status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=30)
    def __str__(self):
        return self.status_name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
    order_date = models.DateTimeField()

class OrderStatus(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT)
    sdate = models.DateTimeField()
    edate = models.DateTimeField()
    order_status_id = models.ForeignKey(Status, on_delete=models.PROTECT)

class OrderGood(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT)
    goods_id = models.ForeignKey(Good, on_delete=models.PROTECT)
    goods_cnt = models.IntegerField(null=False)

class Cart(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.PROTECT)
    goods_id = models.ForeignKey(Good, on_delete=models.PROTECT)
    goods_cnt = models.IntegerField(null=False, default=0)

# ХЗ зачем этот класс, у меня остатки лежат в Warehouse. Но прикрутил, следуя заданию
class StockBalance(models.Model):
    goods_id = models.OneToOneField(Good, on_delete=models.CASCADE, related_name="balance")
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.goods_id.goods_name}: {self.quantity}"

