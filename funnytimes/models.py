from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=50)
    description=models.CharField(max_length=1000)
    pub_date=models.DateField()
    prod_price=models.IntegerField()
    category = models.CharField(max_length=50,default="")
    sub_cat = models.CharField(max_length=50,default="")
    image = models.ImageField(upload_to="funnytimes/images",default="")

    def __str__(self) -> str:
        return self.product_name