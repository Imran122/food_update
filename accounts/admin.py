from django.contrib import admin
from .models import UserProfile,PremiumUser
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(PremiumUser)