from sqlalchemy.orm import Session
from configs.celery_config import app
from db.postgres import engine
from db.models import User
from logger.logger import logger


@app.task
def process_autopayments():
    try:
        with Session(bind=engine) as db:
            # Логика для обработки автоплатежей
            users = db.query(User).filter(User.autopay_enabled == True).all()
            for user in users:
                # Пример логики автоплатежей
                logger.info(f"Обрабатывается автоплатеж для пользователя {user.id}")
    except Exception as e:
            logger.error(f"Ошибка при обработке автоплатежей для пользователя {user.id}: {e}", exc_info=True)
