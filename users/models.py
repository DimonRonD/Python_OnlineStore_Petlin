from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  pass

class Brand(models.Model):
  brand_id = models.AutoField(primary_key=True)
  brand_name = models.CharField(max_length=100)
  def __str__(self):
    return self.brand_name

class Goods_category(models.Model):
  goods_category_id = models.AutoField(primary_key=True)
  category_name = models.CharField(max_length=50)
  def __str__(self):
    return self.category_name


class Goods(models.Model):
  goods_id = models.AutoField(primary_key=True)
  goods_name = models.CharField(max_length=255)
  goods_descr = models.TextField()
  goods_price = models.DecimalField(max_digits=12, decimal_places=2)
  goods_img = models.ImageField(upload_to='goods/')
  goods_category_id = models.ForeignKey('Goods_category', on_delete=models.PROTECT)
  brand_id = models.ForeignKey('Brand', on_delete=models.PROTECT)

  def __str__(self):
    return f"{self.brand_id.brand_name} {self.goods_name}"

class Warehouse(models.Model):
  warehouse_id = models.IntegerField(null=False)
  goods_id = models.ForeignKey('Goods', on_delete=models.PROTECT)
  goods_cnt = models.IntegerField(null=False)
  def __str__(self):
    return f"{self.goods_id}: {self.goods_cnt}"

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
  def __str__(self):
    return self.status_name

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

