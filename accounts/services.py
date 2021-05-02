from django.conf import settings
from twilio.rest import Client
from django.http import HttpResponse


class Twilio:
    def send_meal_plan()