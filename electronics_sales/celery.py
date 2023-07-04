import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electronics_sales.settings')

app = Celery('electronics_sales')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'increase-debt-every-3-hours': {
        'task': 'company.tasks.increase_debt_to_supplier',
        'schedule': crontab(minute=0, hour='*/3'),
    },
    'reduce-debt-daily_at_6_30': {
        'task': 'company.tasks.reduce_debt_to_supplier',
        'schedule': crontab(minute=30, hour=6),
    }
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
