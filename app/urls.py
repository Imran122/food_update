from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('pages.urls')),
    path('test/', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('recipe/', include('recipes.urls')),
    path('accounts/', include('accounts.urls')),
    path('cal/', include('cal.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)