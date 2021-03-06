"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.1.15.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os
from pathlib import Path
from urllib.parse import urlparse
from celery.schedules import crontab

import sys
import environ

#env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR = os.path.join(BASE_DIR,'static')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = env.str('SECRET_KEY')

SECRET_KEY="SJKFLSKFJSKFJKJ453405U3409SAFKFSDF"


# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = env.bool("DEBUG", default=True)
DEBUG = True
#ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'pages',
    'accounts',
    'django_static_jquery',
    'recipes',
    'django_celery_beat',
    'django_celery_results',
    'celery_once',
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   
]

"""
 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    """


CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = ''


ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

'''
DATABASES = {
    'default': {**env.db(), **{'ENGINE': 'django.db.backends.postgresql'}}
}

'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    STATIC_DIR,
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

AUTH_USER_MODEL = 'core.User'

"""
CACHES = {
        'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1;11211',
        'TIMEOUT': 1800,
    }
}
"""
"""
REDIS_HOST='db-redis-nyc3-19343-do-user-8998909-0.b.db.ondigitalocean.com'
REDIS_PORT='25061'
REDIS_PASSWORD='a2p2rhrg5cg0aghj'
"""
"""
BROKER_URL = 'rediss://default:a2p2rhrg5cg0aghj@private-db-redis-nyc3-19343-do-user-8998909-0.b.db.ondigitalocean.com:25061/0?ssl_cert_reqs=CERT_NONE'
CELERY_RESULT_BACKEND = 'rediss://default:a2p2rhrg5cg0aghj@private-db-redis-nyc3-19343-do-user-8998909-0.b.db.ondigitalocean.com:25061/0?ssl_cert_reqs=CERT_NONE'
"""
BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'


CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'



STRIPE_PUBLIC_KEY = ""
STRIPE_SECRET_KEY = ""
STRIPE_WEBHOOK_SECRET=""

LOGIN_REDIRECT_URL='/accounts/login/'
LOGIN_URL='/accounts/login/'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IMPORTS = ('app.tasks','progress.tasks', 'pages.tasks')
CELERY_ONCE = {
      'backend': 'celery_once.backends.Redis',
      'settings': {
        'url': 'redis://redis:6379',
        'default_timeout': 60 * 60
      }
    }

CELERY_TIMEZONE = 'America/New_York'
CELERY_BEAT_SCHEDULE = {
    'send-notification-every-morning': { 
         'task': 'app.tasks.send_notification', 
         'schedule': crontab(hour=7),
        },      
}

TWILIO_ACCOUNT_SID = 'ACf1d40c42d942e44cbb52bd01e4409343'
TWILIO_AUTH_TOKEN = '802ff4a0270c490de597de42f43524b5'
TWILIO_NUMBER = '+17192458173'