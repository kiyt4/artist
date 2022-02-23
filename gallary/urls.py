from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from.import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name="signup"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('cart',views.cart,name="cart"),
    path('order',views.orderd,name="order"),
    path('checout',views.checkout,name="checkout"),
    path('user',views.user,name="user")
]