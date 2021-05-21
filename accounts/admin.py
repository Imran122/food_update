from django.contrib import admin
from .models import UserProfile,PremiumUser,payment_history
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(PremiumUser)
admin.site.register(payment_history)