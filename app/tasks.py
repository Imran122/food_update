from celery.decorators import task
from celery.utils.log import get_task_logger
from time import sleep, time
from celery import shared_task
from celery_progress.backend import ProgressRecorder



logger = get_task_logger(__name__)
@task(name='my_first_task')
def my_first_task(duration):
    sleep(duration)
    return('first_task_done')

def backoff(attempts):
    return 2 ** attempts

@task(bind=True, max_retries=4)
def data_extractor(self):
    try:
        for i in range(1, 11):
            print('Crawling HTML DOM')
            if i == 5:
                raise ValueError('Crawling index error')
    except Exception as exc:
        print('There was an exception lets retry after 5 seconds')
        raise self.retry(exc=exc, countdown=backoff(self.request.retries))


@shared_task(bind=True)
def my_task(self, seconds):
    progress_recorder = ProgressRecorder(self)
    result = 0
    for i in range(seconds):
        sleep(1)
        result += i
        progress_recorder.set_progress(i + 1, seconds)
    return result

@shared_task(bind=True) 
def send_notifiction(self):
     print('Here I am')
     # Another trick