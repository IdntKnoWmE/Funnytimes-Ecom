

from distutils.command.register import register
from django.shortcuts import render
from django.http import HttpResponse
from numpy import product
from .models import Product,Contact,Order,Track_order
import math
import json

# Create your views here.
def index(request):
    product = Product.objects.all()
    #print(product)
    c=math.ceil(len(product)/3)
    return render(request,"funnytimes/index.html",{'range':list(range(0,c,3)),'products':product})

def about(request):
    return render(request,"funnytimes/about.html")

def contact(request):

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        descr = request.POST.get('descr')

        contact = Contact(name=name,email=email,phone=phone,desc=descr)
        contact.save()
    return render(request,"funnytimes/contact.html")


def tracker(request):
    iftrack = False
    tracks = []
    o = []
    if request.method == "POST":
        order_id = request.POST.get("order_id")
        order_email = request.POST.get("order_email")

        try:
            name,or_id = order_id.split("_")
            or_id = int(or_id)
        except:
            return HttpResponse("Wrong order ID")

        order = Order.objects.filter(order_id=or_id,cust_email=order_email)
        iftrack = True
        if len(order)>0:
            track = Track_order.objects.filter(order_id=order_id)
            o = order[0].order_items
            for item in track:
                tracks.append({'update':item.track_desc,'time':item.track_time})
        else:
            return HttpResponse("No such order found.")
        
        

    #print(tracks,iftrack)
    print(o)  
    return render(request,"funnytimes/tracker.html",{'iftrack':iftrack,'tracks':tracks,'order':o})


def prodview(request,id):
    #fetch all info about the prouct_id = id
    fetch = Product.objects.filter(product_id=id)
    return render(request,"funnytimes/productview.html",{'prod':fetch[0]})

def checkout(request):
    thanks = False

    if request.method == "POST":
        cust_name = request.POST.get('cust_name')
        cust_email = request.POST.get('cust_email')
        cust_phone = request.POST.get('cust_phone')
        cust_address = request.POST.get('cust_address') + request.POST.get('cust_address2')
        cust_city = request.POST.get('cust_city')
        cust_zip = request.POST.get('cust_zip')
        cust_state = request.POST.get('cust_state')
        cust_country = request.POST.get('cust_cont')
        order_items = request.POST.get('order_items')

        order = Order(cust_name=cust_name,cust_email=cust_email,cust_phone=cust_phone,cust_address=cust_address,cust_city=cust_city,
        cust_zip=cust_zip,cust_state=cust_state,cust_country=cust_country,order_items=order_items)
        order.save()

        cust_name = cust_name.replace(" ","").lower()
        track_order = Track_order(order_id=cust_name+"_"+str(order.order_id),track_desc="The Order has been Placed.")
        track_order.save()

        thanks = True
        o_id = cust_name + "_" + str(order.order_id)
        return render(request,"funnytimes/checkout.html",{'thanks':thanks,'o_id':o_id})
        
    return render(request,"funnytimes/checkout.html",{"thanks":thanks})


def search(request):
    return render(request,"funnytimes/search.html")
def login(request):
    return render(request,"funnytimes/login.html")
def signup(request):
    return render(request,'funnytimes/signup.html')


def resume(request):
    return render(request,"funnytimes/Resume.html")