from pkg.repositories import autopayments as autopayments_repository
from logger.logger import logger


# Создать автоплатеж
def create_autopayment(user_id: int, amount: float, service_id: int):
    autopayment_data = {
        "user_id": user_id,
        "amount": amount,
        "service_id": service_id
    }
    autopayment = autopayments_repository.create_autopayment(autopayment_data)
    logger.info(f"Autopayment created for user_id={user_id}, service_id={service_id}, amount={amount}")
    return autopayment


# Обновить автоплатеж
def update_autopayment(autopayment_id: int, updates: dict):
    autopayment = autopayments_repository.update_autopayment(autopayment_id, updates)
    if not autopayment:
        logger.error(f"Autopayment with id {autopayment_id} not found")
        return None
    logger.info(f"Autopayment {autopayment_id} updated successfully")
    return autopayment
