from django.contrib import admin
from funnytimes.models import Contact, Product, Order , Track_order


# Register your models here.
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(Track_order)
