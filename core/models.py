from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin

from decimal import *
from datetime import datetime



class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    spoonApi = models.CharField(max_length=255, null=True, blank=True)
    spoonHash = models.CharField(max_length=255, null=True, blank=True)
    

    objects = UserManager()

    USERNAME_FIELD = 'email'

class UserNeeds(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weightLbs = models.DecimalField(blank=True, decimal_places=2, max_digits=10)
    weightKgs = models.DecimalField(blank=True, decimal_places=2, max_digits=10)
    dailyProteinPerKg = models.DecimalField(blank=True, decimal_places=2, max_digits=10)
    dailyCarbPerKg = models.DecimalField(blank=True, decimal_places=2, max_digits=10)
    dailyFatPerKg = models.DecimalField(blank=True, decimal_places=2, max_digits=10)
    dailyProteinNeed = models.DecimalField(blank=True, decimal_places=2, max_digits=10)
    dailyCarbsNeed = models.DecimalField(blank=True, decimal_places=2, max_digits=10)
    dailyFatNeed = models.DecimalField(blank=True, decimal_places=2, max_digits=10)

    lbstoKg = Decimal(2.20462)


    def save(self, *args, **kwargs): 
        print('new one')
        count = 0
        if self.weightLbs is not None: 
            print('in the first if')
            
            self.weightKgs = self.weightLbs / self.lbstoKg
            print(self.weightKgs)            

        else: 
            print('already there')

        if self.dailyProteinNeed is None or self.dailyCarbsNeed is None or self.dailyFatNeed is None:
            print('in the second if')
            self.dailyProteinNeed = self.dailyProteinPerKg * self.weightKgs
            self.dailyCarbsNeed = self.dailyCarbPerKg * self.weightKgs
            self.dailyFatNeed = self.dailyFatPerKg * self.weightKgs

        if self.dailyProteinNeed is not None or self.dailyCarbsNeed is not None or self.dailyFatNeed is not None:
            print('doing stuff')
            self.dailyProteinNeed = self.dailyProteinPerKg * self.weightKgs
            self.dailyCarbsNeed = self.dailyCarbPerKg * self.weightKgs
            self.dailyFatNeed = self.dailyFatPerKg * self.weightKgs

        super(UserNeeds, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.email








