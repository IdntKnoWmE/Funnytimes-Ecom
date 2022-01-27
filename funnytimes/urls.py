
from django.urls import path
from funnytimes import views


urlpatterns = [
    path('',views.index,name="home"),
    path('about',views.about,name="about"),
    path('contact',views.contact,name="contact"),
    path('tracker',views.tracker,name="trackingstatus"),
    path('productview',views.prodview,name="productview"),
    path('checkout',views.checkout,name="checkout"),
    path('search',views.search,name="searchprod"),
    path('login',views.login,name="login"),
    path('signup',views.signup,name="signup")
]
