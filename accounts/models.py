
from django.db import models
#from django.contrib.auth.models import User
from django.utils import timezone
import datetime 
from core.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta

# Create your models here.

# class Package(models.Model):
#       name = models.CharField(max_length=100)
#       price = models.IntegerField(default=0)
      
#       regular_price = models.IntegerField(default=0,blank=True,null=True)
#       create_date = models.DateTimeField(auto_now=True)
#       def __str__(self):
#             return self.name
SUBSCRIPTION =(
      ('F', 'FREE'),
      ('M', 'MONTHLY'),
      ('Y', 'YEARLY'),
)
class UserProfile(models.Model):
      user = models.OneToOneField(User,on_delete=models.CASCADE)
      #photo = models.ImageField(upload_to='photos/%Y/%m/%d',null=True,blank=True,default="../static/img/theme/light/team-1-800x800.jpg")
      expire_date = models.DateTimeField(null=True,blank=True)
      subscription_type= models.CharField(max_length=100,choices=SUBSCRIPTION,default="FREE")
      is_pro = models.BooleanField(default=False)
      def __str__(self):
            return self.user.email



@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance,expire_date=datetime.now()+timedelta(days=30))
    


class PremiumUser(models.Model):
      subscriber_user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
      due_date = models.DateTimeField(default=timezone.now)
      is_premium = models.BooleanField(default=False)
      is_basic = models.BooleanField(default=False)
      is_free = models.BooleanField(default=True)
      create_date = models.DateTimeField(auto_now=True)
      def __str__(self):
            return self.subscriber_user.username