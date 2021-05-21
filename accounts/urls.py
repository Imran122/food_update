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
    path('stripe_charge/',views.stripe_charge,name='stripe_charge'),
    path('cancel_subscription/',views.cancel_subscription,name='cancel_subscription'),
    path('stripe_webhook/',views.stripe_webhook,name = 'stripe_webhook'),
    path('paypal_webhook/',views.paypal_webhook,name='paypal_webhook') 

]
