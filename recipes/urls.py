
from django.urls import path, re_path, include
from . import views
from django.conf.urls import url




urlpatterns = [
    path('<int:recipe_id>', views.recipe, name='recipe'),
    path('recipe_search', views.recipe_search, name='recipe_search'),
    path('faq', views.faq, name='faq'),
    url(r'^ajax/user_favorite/$', views.user_favorite, name='user_favorite'),
    url(r'^ajax/user_yuk/$', views.user_yuk, name='user_yuk'),
    re_path(r'^celery-progress/', include('celery_progress.urls'))
]