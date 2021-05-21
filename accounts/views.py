from requests.auth import HTTPBasicAuth
from django.shortcuts import render,redirect
#from django.contrib.auth.models import User
from core.models import User
from django.http import HttpResponse
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import UserProfile,PremiumUser,payment_history
import stripe
import datetime
import json
import requests
from datetime import datetime,timedelta
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
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
      plan = UserProfile.objects.get(user=request.user).get_subscription_type_display()
      return render(request, 'accounts/cart.html',{'plan':plan})


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


  endpoint = "https://api-m.sandbox.paypal.com/v1/billing/subscriptions/"+identify
  #data = {"ip": "1.1.2.3"}
  auth=HTTPBasicAuth('AcmTDKMC-xKanYmr8hR_i4odVvu48TtyB7wC3ZtNFBqMr-Y2niQ6SZYVqHg3vqPS81mI1e7SwdO2fnrs','EIUoptb1JcphF_jSBOlmvAK-Hyd8JintmFvzDJxhtSp1czl9VaoctL2cyPxpRUJuPWpxTV4UD99pLoKW')

  headers = {"Content-Type":"application/json"}


  get_validation=requests.get(endpoint, auth=auth, headers=headers).json()
  

  if get_validation != '':
    pass
  else:
    return redirect('dashboard')

  sel_user_profile = UserProfile.objects.get(user=request.user)

  if pkg == 'MONTHLY':
    sel_user_profile.customer_email = str(request.user.email)
    sel_user_profile.payment_id = str(identify)
    sel_user_profile.subscription_type = 'M'
    sel_user_profile.payment_type = 'P'
    sel_user_profile.expire_date = datetime.now()+timedelta(days=30)
    sel_user_profile.is_pro = True
    sel_user_profile.save()

  if pkg == 'YEARLY':
    sel_user_profile.customer_id = str(identify)
    sel_user_profile.customer_email = str(request.user.email)
    sel_user_profile.payment_id = str(identify)
    sel_user_profile.subscription_type = 'Y'
    sel_user_profile.payment_type = 'P'
    sel_user_profile.expire_date = datetime.now()+timedelta(days=365)
    sel_user_profile.is_pro = True
    sel_user_profile.save()

  return render(request,'accounts/payment-success.html')


#charging credit card with stripe token 
def stripe_charge(request):

  stripe.api_key = "sk_test_51IbOA2JIiVT83Jh6jFfGGiIHVCqJtO6NHO0bTO4Ca0YsILC0znv1dZVL0pQUCOpiQE0J6LrA8xNfn55G2YTNPYJi00rVVcHrZU"

  pkg=request.COOKIES['package']
  sel_user_profile = UserProfile.objects.get(user=request.user)

  if request.method=='POST':
    stripe_token = request.POST['stripeToken']

  if pkg == 'MONTHLY':
    create_customer = stripe.Customer.create(
                email = str(request.user.email),
                source = str(stripe_token),
                

              )
    
    customer_obj = create_customer
    
    if customer_obj.id :
      create_subscription=stripe.Subscription.create(
              customer=str(customer_obj.id),
              items=[
                {"price": "price_1IddeXJIiVT83Jh6ZjYwkt9R"},
              ],
              
            )

      if create_subscription.id:
        sel_user_profile.customer_id = str(customer_obj.id)
        sel_user_profile.customer_email = str(request.user.email)
        sel_user_profile.payment_id = str(create_subscription.id)
        sel_user_profile.subscription_type = 'M'
        sel_user_profile.payment_type = 'S'
        sel_user_profile.expire_date = datetime.now()+timedelta(days=30)
        sel_user_profile.is_pro = True
        sel_user_profile.save()

    return HttpResponse("<h1>Monthly subscription successful with stripe</h1>")

  if pkg == 'YEARLY':
    create_customer = stripe.Customer.create(
                email = str(request.user.email),
                source = str(stripe_token),
                

              )
    
    customer_obj = create_customer
    
    if customer_obj.id :
      create_subscription=stripe.Subscription.create(
              customer=str(customer_obj.id),
              items=[
                {"price": "price_1IddeXJIiVT83Jh6H65xxWLG"},
              ],
              
            )

      if create_subscription.id:
        sel_user_profile.customer_id = str(customer_obj.id)
        sel_user_profile.customer_email = str(request.user.email)
        sel_user_profile.payment_id = str(create_subscription.id)
        sel_user_profile.subscription_type = 'Y'
        sel_user_profile.payment_type = 'S'
        sel_user_profile.expire_date = datetime.now()+timedelta(days=365)
        sel_user_profile.is_pro = True
        sel_user_profile.save()

    return HttpResponse("<h1>YEARLY subscription successful with stripe</h1>")







def cancel_subscription(request):
  sel_profile = UserProfile.objects.get(user=request.user)
  stripe.api_key = "sk_test_51IbOA2JIiVT83Jh6jFfGGiIHVCqJtO6NHO0bTO4Ca0YsILC0znv1dZVL0pQUCOpiQE0J6LrA8xNfn55G2YTNPYJi00rVVcHrZU"
  subscription = sel_profile.subscription_type
  plan = sel_profile.payment_type
  if subscription == 'F' :
    return redirect('cart')

  if plan == 'S':
    subscription_id = str(sel_profile.payment_id)
    cancel=stripe.Subscription.delete(subscription_id)

    if cancel.status == 'canceled':
      sel_profile.expire_date = datetime.now()+timedelta(days=30)
      sel_profile.subscription_type = 'F'
      sel_profile.payment_type = 'F'
      sel_profile.customer_id = None
      sel_profile.payment_id = None
      sel_profile.is_pro = False
      sel_profile.save()

      return HttpResponse('<h1>Subscription has been canceled !</h1>')

    else :
      return HttpResponse('<h1>sorry , something went wrong</h1>')


  if plan == 'P':
    subscription_id = str(sel_profile.payment_id)
    endpoint = "https://api-m.sandbox.paypal.com/v1/billing/subscriptions/"+subscription_id+"/cancel"
    data = {"reason":"client is not Not satified"}
    auth=HTTPBasicAuth('AcmTDKMC-xKanYmr8hR_i4odVvu48TtyB7wC3ZtNFBqMr-Y2niQ6SZYVqHg3vqPS81mI1e7SwdO2fnrs','EIUoptb1JcphF_jSBOlmvAK-Hyd8JintmFvzDJxhtSp1czl9VaoctL2cyPxpRUJuPWpxTV4UD99pLoKW')
    headers = {"Content-Type":"application/json"}
    #r_headers = {"Authorization": "Basic AcmTDKMC-xKanYmr8hR_i4odVvu48TtyB7wC3ZtNFBqMr-Y2niQ6SZYVqHg3vqPS81mI1e7SwdO2fnrs:EIUoptb1JcphF_jSBOlmvAK-Hyd8JintmFvzDJxhtSp1czl9VaoctL2cyPxpRUJuPWpxTV4UD99pLoKW"}
    #print('your endnpoint is',endpoint,'and paymetn id ',subscription_id)
    cancel_request=requests.post(endpoint,data=json.dumps(data),auth=auth,headers=headers)

    print('cancel data',cancel_request)
    print(endpoint)

    if cancel_request.status_code == 204:
      sel_profile.expire_date = datetime.now()+timedelta(days=30)
      sel_profile.subscription_type = 'F'
      sel_profile.payment_type = 'F'
      sel_profile.customer_id = None
      sel_profile.payment_id = None
      sel_profile.is_pro = False
      sel_profile.save()
      return HttpResponse('<h1>paypal subscription canceled successfully</h1>')

    else :
      print('your request is',cancel_request)
      return HttpResponse('<h1>something went wrong </h1>')





@csrf_exempt
def stripe_webhook(request):
  if request.method == 'GET':
    return HttpResponse('<h1>stripe webhook is working</h1>')
  if request.method == 'POST':
    event = None
    payload = request.body
    try:
        event = json.loads(payload)
        
        if event['type'] == 'charge.succeeded':
          customer = str(event['data']['object']['source']['customer'])
          email=UserProfile.objects.get(customer_id=customer).user.email

          payment_history.objects.create(user=email,order=event['created'],payment_method = 'Card Payment',amount=(event['data']['object']['amount']/100))

          detect_plan = (event['data']['object']['amount']/100)
          if int(detect_plan) == 3:
            update=UserProfile.objects.get(user__email=email)
            update.expire_date = datetime.now()+timedelta(days=30)
            update.save()

          if int(detect_plan) == 30 :
            update=UserProfile.objects.get(user__email=email)
            update.expire_date = datetime.now()+timedelta(days=365)
            update.save()



          return HttpResponse(status = 200)
        return HttpResponse(status=200)
    except:
        print('Webhook error while parsing basic request.' + str(e))
        return HttpResponse(status = 400)




@csrf_exempt
def paypal_webhook(request):
  if request.method == 'GET':
    return HttpResponse('<h1>stripe webhook is working</h1>')
  if request.method == 'POST':
    event = None
    payload = request.body
    #print(payload)
    
    if 1==1:
        event = json.loads(payload)
        
        if event['event_type'] == 'BILLING.SUBSCRIPTION.ACTIVATED':
          customer_payment_id = str(event['resource']['id'])
          
          sel=UserProfile.objects.get(payment_id=customer_payment_id)
          email = sel.user.email
          subtype=sel.get_subscription_type_display()
          
          
          

          #get_amount = jsonify['billing_cycles']['frequency']['pricing_scheme']['fixed_price']['value']

          



          detect_plan = subtype
          if str(detect_plan) == 'MONTHLY':
            update=UserProfile.objects.get(user__email=email)
            update.expire_date = datetime.now()+timedelta(days=30)
            update.save()
            payment_history.objects.create(user=email,order=customer_payment_id,payment_method = 'Paypal',amount=3)


          if str(detect_plan) == 'YEARLY' :
            update=UserProfile.objects.get(user__email=email)
            update.expire_date = datetime.now()+timedelta(days=365)
            update.save()
            payment_history.objects.create(user=email,order=customer_payment_id,payment_method = 'Paypal',amount=30)




          return HttpResponse('ok')
        return HttpResponse('ok')
    





def logout(request):
  auth.logout(request)
  return redirect('login')