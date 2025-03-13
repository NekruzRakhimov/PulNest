from celery.schedules import crontab
from celery import Celery

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

app.conf.beat_schedule = {
    'run_autopayments_every_day': {
        'task': 'tasks.autopayments.process_autopayments',
        'schedule': crontab(minute="0", hour="17"),  # каждый день в 17:00
    }
}

app.conf.broker_connection_retry_on_startup = True

# Автоматическое обнаружение задач в пакете tasks
app.autodiscover_tasks(['tasks'])
