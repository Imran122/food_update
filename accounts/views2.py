
from django.shortcuts import render,redirect
#from django.contrib.auth.models import User
from core.models import User
from django.http import HttpResponse
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import UserProfile,PremiumUser,payment_history
import stripe
import datetime

from datetime import datetime,timedelta
from django.utils import timezone
stripe.verify_ssl_certs = False


def account_history(request):
	if request.method == 'GET':

		sel_history = payment_history.objects.filter(user=request.user.email)
		return render(request, 'accounts/account_history.html',{'history':sel_history})

def change_card(request):
	if request.method == 'GET':
		return render(request, 'accounts/change_card.html')

	if request.method == 'POST':
		get_token = request.POST['stripeToken']
		try:

			get_customer = UserProfile.objects.get(user=request.user).customer_id
			if get_customer == None :
				return HttpResponse('<h1>You are not premium customer yet !</h1>')
		except :
			return HttpResponse('<h1> You are not premium customer yet !</h1>')
		stripe.api_key = "sk_test_51IbOA2JIiVT83Jh6jFfGGiIHVCqJtO6NHO0bTO4Ca0YsILC0znv1dZVL0pQUCOpiQE0J6LrA8xNfn55G2YTNPYJi00rVVcHrZU"
		mod=stripe.Customer.modify(
				  str(get_customer),
				  source = str(get_token)
				  
				)

		if mod.id :
			return HttpResponse('<h1> Default Card for subscription has been changed !</h1>')

		else :
			return HttpResponse('<h1>Sorry , can not change your card </h1>')

