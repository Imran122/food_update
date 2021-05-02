from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from recipes import models

# Register your models here.

admin.site.register(models.RecipeOverview)
admin.site.register(models.Ingredient)
admin.site.register(models.Direction)
admin.site.register(models.Events)
admin.site.register(models.UserInterest)
admin.site.register(models.ShoppingList)
admin.site.register(models.ShoppingListItem)
admin.site.register(models.DayIntensity)