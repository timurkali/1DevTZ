import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')

app = Celery('delivers_celery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every-5-seconds': {
        'task': 'basic.tasks.my_periodic_task',
        'schedule': 5,  # seconds
    },
    "every-day": {
        "task": "basic.tasks.my_scheduled_task",
        "schedule": crontab(hour=17, minute=58,)  # Asia/Almaty timezone
    },
}
