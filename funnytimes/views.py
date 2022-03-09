

from distutils.command.register import register
from http import client
from locale import currency
from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse
from numpy import product
from .models import Product,Contact,Order,Track_order
import math
import json
import razorpay
from django.views.decorators.csrf import csrf_exempt


#create razorpay client
razorpay_client = razorpay.Client(auth=('rzp_test_Z0Lhe1QTy1gvQE','vGBLnePxznOuAFIYIgY1Fh7p'))

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
        order_price = request.POST.get('order_price')


        #create razorpay order id
        response_payment = razorpay_client.order.create(dict(amount=int(order_price)*100,currency='INR'))

        razorpay_order_id = response_payment['id']
        order_status = response_payment['status']

        if order_status == 'created':
            order = Order(cust_name=cust_name,cust_email=cust_email,cust_phone=cust_phone,cust_address=cust_address,cust_city=cust_city,
            cust_zip=cust_zip,cust_state=cust_state,cust_country=cust_country,order_items=order_items,order_price=order_price,razor_order_id=razorpay_order_id)
            order.save()


            return payment(request,info=[int(order_price)*100,razorpay_order_id,cust_name,cust_email,cust_phone])

            '''
            cust_name = cust_name.replace(" ","").lower()
            track_order = Track_order(order_id=cust_name+"_"+str(order.order_id),track_desc="The Order has been Placed , Thankyou . . .")
            track_order.save()
            

            thanks = True
            o_id = cust_name + "_" + str(order.order_id)
            return render(request,"funnytimes/checkout.html",{'thanks':thanks,'o_id':o_id})
            '''
            
        
    return render(request,"funnytimes/checkout.html")


def search(request):
    return render(request,"funnytimes/search.html")
def login(request):
    return render(request,"funnytimes/login.html")
def signup(request):
    return render(request,'funnytimes/signup.html')

def payment(request,info):
    
    pay_info = {
        'amount':info[0],
        'razorder_id':info[1],
        'cust_name':info[2],
        'cust_email':info[3],
        'cust_phone':info[4],
    }
    return render(request,'funnytimes/payment.html',pay_info)


@csrf_exempt
def payment_status(request):

    response = request.POST
    payment_id = response['razorpay_payment_id']
    razorp_order_id = response['razorpay_order_id']
    signature = response['razorpay_signature']
    params_dict = {
        'razorpay_order_id': razorp_order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }

    # verify the payment signature.
    
    try:
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        fetch_order = Order.objects.get(razor_order_id = razorp_order_id)
        fetch_order.razor_payment_id = payment_id
        fetch_order.paid = True
        fetch_order.save()


        cust_name = fetch_order.cust_name
        cust_name = cust_name.replace(" ","").lower()
        track_order = Track_order(order_id=cust_name+"_"+str(fetch_order.order_id),track_desc="The Order has been Placed. ")
        track_order.save()
        track_order = Track_order(order_id=cust_name+"_"+str(fetch_order.order_id),track_desc="Online payment done successfully. ")
        track_order.save()
            
        o_id = cust_name + "_" + str(fetch_order.order_id)

        return render(request,'funnytimes/payment_status.html',{'verify':True,'o_id':o_id})




    #print(response)
    except:
        return render(request,'funnytimes/payment_status.html',{'verify':False})
        


def resume(request):
    return render(request,"funnytimes/Resume.html")