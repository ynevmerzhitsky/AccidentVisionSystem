import os
from celery import Celery
from kombu import Queue
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accidentvision.settings')
broker = settings.BROKER_URL
app = Celery('accidentvision', broker=broker)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_queues = (
    Queue('task', routing_key='task'),
)
app.autodiscover_tasks()