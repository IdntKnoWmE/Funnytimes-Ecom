
from distutils.command.register import register
from http import client
from lib2to3.pgen2.tokenize import generate_tokens
from locale import currency
from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse
from numpy import product

from ecom import settings
from .models import Product,Contact,Order,Track_order
import math
import json
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from . tokens import generate_token


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
    #print(o)  
    return render(request,"funnytimes/tracker.html",{'iftrack':iftrack,'tracks':tracks,'order':o})


def prodview(request,id):
    #fetch all info about the prouct_id = id
    fetch = Product.objects.filter(product_id=id)
    return render(request,"funnytimes/productview.html",{'prod':fetch[0]})

def checkout(request):

    if not request.user.is_authenticated:
        messages.info(request, "Please Login for checking out!")
        return redirect('home')

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

def searchMatch(query, item):
    des = item.description.lower()
    nam = item.product_name.lower()
    cate = item.category.lower()
    #print(des,nam,cate)
    for q in query:
        q=q.lower()
        common_words = ['a','in','to','the','of','and','for','by','on','is',
        'i','all','this','with','it','at','from','or','you','as','your','an',
        'are','be','that','do','not','have','can','was','if','we','but','what',
        'which','there','when','use','their','they','how','he','were','his','had',
        'each','said','she','word']

        if q in common_words:
            continue
        if q in des or q in nam or q in cate:
            return True
    return False

def search(request):

    if request.method == 'GET':

        qu = request.GET.get('search')
        query = set(qu.split())
        
        all_product = Product.objects.all()

        prod=[]
        for item in all_product:

            if searchMatch(query, item):
                prod.append(item)
        
        c=math.ceil(len(prod)/3)
        return render(request,"funnytimes/search.html",{'range':list(range(0,c,3)),'products':prod,'query':qu})
    
        
    return HttpResponse('404 - NotFound! ')

#@login_required(login_url='/funnytimes/')
def profile(request):
    return render(request,"funnytimes/profile.html")


#@login_required(login_url='/funnytimes/')
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request, "Successfully logged out")
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found!')

def login(request):

    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_password = request.POST['password']
        user=authenticate(username= user_id, password= user_password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")


    else:
        return HttpResponse("404 -  Not Found!")


def signup(request):
    if request.method=='POST':
        user_fname = request.POST['fname']
        user_lname = request.POST['lname']
        user_email = request.POST['email'].lower()
        user_passw = request.POST['passw']

        if User.objects.filter(username=user_email).exists():
            messages.error(request,'Account already exist...')
            return redirect('home')

        else:

            myuser = User.objects.create_user(user_email,user_email,user_passw)
            myuser.first_name = user_fname
            myuser.last_name = user_lname
            myuser.is_active=False
            myuser.save()

            #confirmation email sent code
            current_site_domain = get_current_site(request)
            email_subject = 'Confirm your account @ funny-times Login!'

            message = render_to_string('email_confirm.html',{
                'name':myuser.first_name,
                'domain':current_site_domain,
                'unique_id':urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token' : generate_token.make_token(myuser)
            })

            email = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )

            email.fail_silently =True
            email.send()


            messages.info(request,'Confirmation link has been send to your Email id.')
            messages.info(request,'Please confirm it for login!')
            return redirect('home')

    else:
        return HttpResponse('404 - Not Found!')

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


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except:
        myuser = None
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()

        auth_login(request,myuser)
        messages.success(request,'Congrats! Your account has been Verified')
        return redirect('home')
    
    else:
        return HttpResponse('Error! 404')
