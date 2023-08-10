import logging
import os

from celery import Celery
from django.conf import settings

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('celery_service')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND

app.autodiscover_tasks()
