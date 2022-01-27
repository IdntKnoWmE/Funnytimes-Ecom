

from distutils.command.register import register
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
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
    return render(request,"funnytimes/contact.html")
def tracker(request):
    return render(request,"funnytimes/tracker.html")
def prodview(request):
    return render(request,"funnytimes/productview.html")
def checkout(request):
    return render(request,"funnytimes/checkout.html")
def search(request):
    return render(request,"funnytimes/search.html")
def login(request):
    return render(request,"funnytimes/login.html")
def signup(request):
    return render(request,'funnytimes/signup.html')