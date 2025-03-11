from celery import Celery

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',   # Используем Redis для очередей
    backend='redis://localhost:6379/0'
)

app.conf.beat_schedule = {
    'run_autopayments_every_day': {
        'task': 'tasks.process_autopayments',
        'schedule': 86400.0  # каждый день
    }
}
