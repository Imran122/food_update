
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


def account_history(request):

      return render(request, 'accounts/account_history.html')

def change_card(request):

      return render(request, 'accounts/change_card.html')