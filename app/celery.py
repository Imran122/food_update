from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.decorators import task
from celery.utils.log import get_task_logger
from time import sleep
os.environ.setdefault('DJANGO_SETTINGS_MODULE','app.settings')
app = Celery('app')
app.conf.ONCE = settings.CELERY_ONCE
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


