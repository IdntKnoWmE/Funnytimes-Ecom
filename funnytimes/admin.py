from re import search
from django.contrib import admin
from django.forms import Textarea
from funnytimes.models import Contact, Product, Order , Track_order
from django.db import models

class order_display(admin.ModelAdmin):
    list_display = ['cust_email','order_id','cust_phone','cust_city','order_date']

    fields = [('cust_name'),('cust_email','cust_phone'),('cust_address','cust_zip'),('cust_city','cust_state','cust_country'),('order_items','order_date'),('order_price'),('razor_payment_id','paid')]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }

    search_fields = ['cust_email','cust_phone']

    list_filter = ['paid']



# Register your models here.
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order,order_display)
admin.site.register(Track_order)
