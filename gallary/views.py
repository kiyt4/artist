from django.shortcuts import  redirect, render
from distutils.log import error
import errno
from importlib.resources import path
from unicodedata import name
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from matplotlib.pyplot import flag
from sympy import re
from.models import  contact_info ,products,category,order
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password


# Create your views here.
def home(request):
    nam=None
    return render (request,'home.html')

def signup(request):
    if request.method =="POST":
        n=request.POST.get('fname')
        d=request.POST.get('lname')
        e=request.POST.get('email')
        f=request.POST.get('mobile')
        g=request.POST.get('password')
        contact= contact_info(fname=n,lname=d,email=e,mobile=f,password=make_password(g))
        
        
        contact.save()
        
        
        
        return redirect('home')
    return render (request,'home.html')



def login(request):
    error_message = None
    if request.method == "POST":
        emails=request.POST.get('email')
        password=request.POST.get('password')
        print(emails)
        try:
            cust_login = contact_info.objects.get(email = emails)
            if cust_login:
                request.session['client_email'] = cust_login.email
                
                flag =check_password(password,cust_login.password)
                if flag:
                    request.session['name'] = cust_login.fname
                    print(request.session['name'])
                    request.session['customer_id']= cust_login.id
                    return redirect('home')
                    
                else:
                    error_message = "Invalid password"
                    return render(request,'home.html',{'error_msg': error_message})
        except:
            error_message = "email is not exits"
            return render('home.html',{'error_msg': error_message})


def checkout(request):
    if request.method =="POST":
        address=request.POST.get("Address")
        phone=request.POST.get("phone")
        customer_id=request.session.get("customer_id")
        cart= request.session.get('cart')
        product=products.objects.filter(id__in=list(cart.keys()))

        for pro in product:
            save_order_dtls = order(
                customer=contact_info(id=customer_id),
                product=pro,
                price=pro.price,
                quntity=cart.get(str(pro.id)),
                Address=address,
                phone=phone)
            # print(phone,address)
            save_order_dtls.save()
            


    return redirect('order')

def cart(request):
    p=list(request.session.get('cart').keys())
    f=products.objects.filter(id__in=p)
    print(p,f)
    return render(request,'cart.html',{'f':f})


def user (request):
    path=None
    # img= product.objects.all()
    if request.method =="POST":
        product_id = request.POST.get('cartid')
        remove= request.POST.get('minus')
        cart_id= request.session.get('cart')
        


        if cart_id:
            quantity= cart_id.get(product_id)
            
            if quantity:
                if remove:
                    if quantity <=1:
                        cart_id.pop(product_id)
                    else:
                        cart_id[product_id] = quantity -1
                else:
                    cart_id[product_id] = quantity +1   
            else:
                cart_id[product_id] = 1
        else:
            cart_id ={}
            cart_id[product_id] = 1
        request.session['cart']= cart_id
        print(request.session['cart'])
        
    cat= category.objects.all()
    cat_id=request.GET.get(category)
    if cat_id:
        path=products.objects.filter(category_id=cat_id)
    else:
        path=products.objects.all()


    return render(request,'user.html',{'products':path,'cate':cat})

def orderd(request):
    customer=request.session['customer_id']
    orderd=order.objects.filter(customer=customer).order_by('-date')
    print(orderd)
    c=0
    for i in products:
        c +=i.price*i.quntity
    print(c)

    return render(request,'order.html',{'order':orderd,'c':c})

def logout(request):
    request.session.clear()
    return redirect('home')