from django.urls import path

from . import views
from django.conf.urls import url

app_name = 'pages'

urlpatterns = [
    #path('', views.index, name='index'), 
    path('dashboard/', views.dashboard, name='dashboard'), 
    #path('home/', views.home, name='home'),    
    #path('register', views.register, name='register'),
    #path('login', views.login, name='login'),
    path('calendar/', views.calendar, name='calendar'),
    path('shoppinglist/<int:list_id>/', views.shopping_list, name='shoppingList'),
    path('plan-create/', views.plan_generate, name='plancreate'),
    path('mealplanview/', views.mealplan_view, name='mealplanView'),
    url(r'ajax/dismiss_shopping_list_item/$', views.dismiss_shopping_list_item, name='dismiss_item'),
    url(r'ajax/lock_status/$', views.meal_plan_lock_status, name='meal_plan_lock_status'),
    url(r'ajax/remove_shopping_list/$', views.remove_shopping_list, name='remove_shopping_list'),
    url(r'ajax/generate_shopping_list/$', views.generate_shopping_list, name='generate_shopping_list'),
    url(r'ajax/feedback_meal/$', views.feedback_meal, name='feedback_meal'),

]

