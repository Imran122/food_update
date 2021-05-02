from django.urls import path

from . import views,views2
from django.conf.urls import url

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),  
    path('signup/', views.signup, name='signup'),  
    path('cart/', views.cart, name='cart'), 
    path('payment-success/',views.payment_success,name='payment_success'),
    path('paypal-payment-success/',views.paypal_payment_success,name='paypal_payment_success'),
    path('logout/',views.logout,name='logout'),
    path('account_history/', views2.account_history, name='account_history'),
    path('change_card/', views2.change_card, name='change_card'),    

]
