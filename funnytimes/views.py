

from distutils.command.register import register
from django.shortcuts import render
from django.http import HttpResponse
from numpy import product
from .models import Product,Contact
import math

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
    return render(request,"funnytimes/tracker.html")
def prodview(request,id):
    #fetch all info about the prouct_id = id
    fetch = Product.objects.filter(product_id=id)
    return render(request,"funnytimes/productview.html",{'prod':fetch[0]})
def checkout(request):
    return render(request,"funnytimes/checkout.html")
def search(request):
    return render(request,"funnytimes/search.html")
def login(request):
    return render(request,"funnytimes/login.html")
def signup(request):
    return render(request,'funnytimes/signup.html')