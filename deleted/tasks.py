from celery import Celery
from celery.signals import setup_logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, User  # Замените на ваш класс модели пользователя
from configs.config import settings
from celery.schedules import crontab

# Настроим Celery с использованием Redis в качестве брокера
app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',   # ЗАМЕНИТЬ на localhost
    backend='redis://localhost:6379/0'   # ЗАМЕНИТЬ на localhost
)


# Расписание для выполнения задач каждый день в полночь
app.conf.beat_schedule = {
    'run_autopayments_every_day': {
        'task': 'tasks.process_autopayments',
        'schedule': crontab(minute=0, hour=0),  # каждый день в 00:00
    }
}

app.conf.broker_connection_retry_on_startup = True


engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@app.task
def process_autopayments():
    # Получение сессии из SQLAlchemy
    db = SessionLocal()
    try:
        # Логика для обработки автоплатежей
        users = db.query(User).filter(User.autopay_enabled == True).all()
        for user in users:
            # Пример логики автоплатежей (добавьте реальную логику)
            print(f"Обрабатывается автоплатеж для пользователя {user.id}")
    except Exception as e:
        print(f"Ошибка при обработке автоплатежей: {e}")
    finally:
        db.close()

# Пример для конфигурации логирования Celery
@setup_logging.connect
def setup_celery_logging(*args, **kwargs):  # <-- Добавлено **kwargs
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
