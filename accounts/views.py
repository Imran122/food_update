
from django.shortcuts import render,redirect
#from django.contrib.auth.models import User
from core.models import User
from django.http import HttpResponse
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import UserProfile,PremiumUser
import stripe
import datetime

from datetime import datetime,timedelta
from django.utils import timezone
stripe.verify_ssl_certs = False

def home(request):

      return render(request, 'accounts/home.html')
#AgentProfile = Agent.objects.get(user=request.user)
def signup(request):
      if request.method == 'POST':
            name = request.POST['name'] 
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            if password == password2:
                  if User.objects.filter(name=name).exists():
                        #messages.error(request, 'That user name already taken')
                        return redirect('signup')
                  else:
                        if User.objects.filter(email=email).exists():
                              #messages.error(request, 'That email already taken')
                              return redirect('signup')
                        else:

                              user = User.objects.create_user(name = name, password=password, email=email,)
                              user.save()
                              
                              return redirect('login')
            else:
                  #messages.error(request, 'passwords not match')
                  return redirect('signup')
      else:

            return render(request, 'accounts/signup.html')
# def signup(request):
#       if request.method == "POST":
#             u_form = UserForm(request.POST)
#             p_form = ProfileForm(request.POST)
#             if u_form.is_valid() and p_form.is_valid():
#                   user = u_form.save()
#                   p_form = p_form.save(commit=False)
#                   p_form.user = user
#                   p_form.save()
#                   print("hello")
#                   return redirect('login')
#       else:
#             u_form = UserForm(request.POST)
#             p_form = ProfileForm(request.POST)
#             context ={
#                   'u_form':u_form,
#                   'p_form':p_form,
#             }
#             return render(request,'accounts/signup.html',context)

def login(request):

      if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                  auth.login(request, user)
                  #messages.success(request, 'you are login')
                  return redirect('pages:dashboard')
            else:
                  #messages.error(request, 'Invalid unser password')
                  return redirect('login')
      else:
            return render(request, 'accounts/login.html')


def check_user_permission(user):
  sel_user_profile = UserProfile.objects.get(user=user)
  return sel_user_profile.expire_date < timezone.now()


@login_required()
def cart(request):
      '''
      if request.method == 'POST':
            membership = request.POST.get('membership', 'MONTHLY')
            amount = 3
            if membership == 'YEARLY':
                  amount = 30
            
      stripe.api_key = "sk_test_51IbOA2JIiVT83Jh6jFfGGiIHVCqJtO6NHO0bTO4Ca0YsILC0znv1dZVL0pQUCOpiQE0J6LrA8xNfn55G2YTNPYJi00rVVcHrZU"

      session = stripe.checkout.Session.create(
              payment_method_types=['card'],
              line_items=[{
                'name': 'Kavholm rental',
                'amount': 3,
                'currency': 'usd',
                'quantity': 1,
              }],
  
  
  mode='payment',
  success_url='https://example.com/success',
  cancel_url='https://example.com/failure',
)
'''
         
      return render(request, 'accounts/cart.html')


@login_required()
def payment_success(request):

      ssid = request.GET['session_id']
      pkg=request.COOKIES['package']


      
      stripe.api_key = "sk_test_51IbOA2JIiVT83Jh6jFfGGiIHVCqJtO6NHO0bTO4Ca0YsILC0znv1dZVL0pQUCOpiQE0J6LrA8xNfn55G2YTNPYJi00rVVcHrZU"

      data=stripe.checkout.Session.retrieve(ssid,)
            
      if data.payment_status != '' :

        sel_user_profile = UserProfile.objects.get(user=request.user)

        if pkg == 'MONTHLY' :
          sel_user_profile.subscription_type = 'M'
          sel_user_profile.expire_date = datetime.now()+timedelta(days=30)
          sel_user_profile.save()

        if pkg == 'YEARLY':
          sel_user_profile.subscription_type = 'Y'
          sel_user_profile.expire_date = datetime.now()+timedelta(days=365)
          sel_user_profile.save()


        return render(request,'accounts/payment-success.html')

      else :
            return HttpResponse('<h1>Payment Error</h1>')

@login_required()
def paypal_payment_success(request):
  pkg=request.COOKIES['package']
  
  identify=request.GET['paymentid']
  if identify == '':
    return redirect('dashboard')
  sel_user_profile = UserProfile.objects.get(user=request.user)
  if pkg == 'MONTHLY':
          sel_user_profile.subscription_type = 'M'
          sel_user_profile.expire_date = datetime.now()+timedelta(days=30)
          sel_user_profile.save()

  if pkg == 'YEARLY':
    sel_user_profile.subscription_type = 'Y'
    sel_user_profile.expire_date = datetime.now()+timedelta(days=365)
    sel_user_profile.save()

  return render(request,'accounts/payment-success.html')



def logout(request):
  auth.logout(request)
  return redirect('login')