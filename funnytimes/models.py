from statistics import mode
from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=50)
    description=models.CharField(max_length=5000)
    pub_date=models.DateField()
    prod_price=models.IntegerField()
    category = models.CharField(max_length=50,default="")
    sub_cat = models.CharField(max_length=50,default="")
    image = models.ImageField(upload_to="funnytimes/images",default="")

    def __str__(self) -> str:
        return self.product_name


class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=70)
    email = models.EmailField(max_length=100)
    phone = models.TextField(max_length=15)
    desc = models.TextField(max_length=500)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    cust_name = models.TextField(max_length=70)
    cust_email = models.EmailField(max_length=100)
    cust_phone = models.TextField(max_length=15)
    cust_address = models.TextField(max_length=500)
    cust_city = models.TextField(max_length=15)
    cust_zip = models.TextField(max_length=15)
    cust_state = models.TextField(max_length=15)
    cust_country = models.TextField(max_length=15)
    order_items = models.TextField(max_length=500)

    def __str__(self) -> str:
        return self.cust_name + "_" + str(self.order_id)


class Track_order(models.Model):
    track_id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=75)
    track_desc = models.CharField(max_length=500)
    track_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.track_desc[:7] + "..."
        