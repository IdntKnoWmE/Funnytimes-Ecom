
from django.urls import path
from funnytimes import views


urlpatterns = [
    path('',views.index,name="home"),
    path('about',views.about,name="about"),
    path('contact',views.contact,name="contact"),
    path('tracker',views.tracker,name="trackingstatus"),
    path('productview/<int:id>',views.prodview,name="productview"),
    path('checkout',views.checkout,name="checkout"),
    path('search',views.search,name="searchprod"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('signup',views.signup,name="signup"),
    path('resume',views.resume,name="resume"),
    path('payment',views.payment,name="payment"),
    path('payment_status',views.payment_status,name='payment_status'),
     path('profile',views.profile,name="profile"),
     path('activate/<uidb64>/<token>',views.activate,name='activate'),
]
