from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  pass

class Goods_category(models.Model):
  goods_category_id = models.AutoField(primary_key=True)
  category_name = models.CharField(max_length=50)
  def __str__(self):
    return self.goods_category_name


class Goods(models.Model):
  goods_id = models.AutoField(primary_key=True)
  goods_name = models.CharField(max_length=255)
  goods_descr = models.TextField()
  goods_price = models.DecimalField(max_digits=7, decimal_places=2)
  goods_img = models.ImageField(upload_to='products/')
  goods_category_id = models.ForeignKey('Category', on_delete=models.PROTECT)

  def str(self):
    return [self.name](http: // self.name /)

 class Warehouse(models.Model):
  warehouse_id = models.IntegerField(null=False)
  goods_id = models.ForeignKey('Goods', on_delete=models.PROTECT)
  goods_cnt = models.IntegerField(null=False)

class Customers(models.Model):
  customer_id = models.AutoField(primary_key=True)
  customer_name = models.CharField(max_length=50)
  customer_surname = models.CharField(max_length=50)
  customer_patronym = models.CharField(max_length=100)
  customer_address = models.TextField()
  customer_email = models.EmailField()
  customer_phone = models.IntegerField()

class Status(models.Model):
  order_status_id = models.AutoField(primary_key=True)
  status_name = models.CharField(max_length=30)

class Orders(models.Model):
  order_id = models.AutoField(primary_key=True)
  customer_id = models.ForeignKey('Customers', on_delete=models.PROTECT)
  order_date = models.DateTimeField()

class Order_status(models.Model):
  order_id = models.ForeignKey('Orders', on_delete=models.PROTECT)
  sdate = models.DateTimeField()
  edate = models.DateTimeField()
  order_status_id = models.ForeignKey('Status', on_delete=models.PROTECT)

class Order_goods(models.Model):
  order_id = models.ForeignKey('Orders', on_delete=models.PROTECT)
  goods_id = models.ForeignKey('Goods', on_delete=models.PROTECT)
  goods_cnt = models.IntegerField(null=False)

class Cart(models.Model):
  customer_id = models.ForeignKey('Customers', on_delete=models.PROTECT)
  goods_id = models.ForeignKey('Goods', on_delete=models.PROTECT)
  goods_cnt = models.IntegerField(null=False)

