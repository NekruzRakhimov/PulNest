from datetime import datetime
from typing import List
from logger.logger import logger
from pkg.repositories import service as service_repository
from schemas.service import ServiceSchema
from db.models import Service

def create_service(service: ServiceSchema):
    try:
        created_service = service_repository.create_service(service.merchant_name, service.category_id)
        return created_service
    except Exception as e:
        logger.error(f"Error creating service for merchant {service.merchant_name}: {e} here is the mistake")
        raise



def get_service_by_id(service_id):
    try:
        service = service_repository.get_service_by_id(service_id)
        if service is not None:
            return service
        else:
            return None
    except Exception as e:
        logger.error(f"Error retrieving service {service_id}: {e}")
        raise


def get_service_by_merchant_name(merchant_name):
    try:
        service = service_repository.get_service_by_merchant_name(merchant_name)
        if service is not None:
            return service
        else:
            return None
    except Exception as e:
        logger.error(f"Error retrieving service for merchant {merchant_name}: {e}")
        raise


def get_all_services():
    try:
        services = service_repository.get_all_services()
        logger.info(f"Retrieved {len(services)} services.")
        return services
    except Exception as e:
        logger.error(f"Error retrieving all services: {e}")
        raise


def deactivate_service(service_id):
    try:
        service = service_repository.update_service(service_id, is_active=False)
        if service is not None:
            logger.info(f"Service {service_id} deactivated.")
            return service
        else:
            return None
    except Exception as e:
        logger.error(f"Error deactivating service {service_id}: {e}")
        raise


def topup_merchant_balance(service_id, amount):
    try:
        service = service_repository.get_service_by_id(service_id)
        if service is not None and amount > 0:
            service.balance += amount
            service.updated_at = datetime.now()
            updated_service = service_repository.update_service(service_id, balance=service.balance)
            logger.info(f"Added {amount} to balance for service {service_id}.")
            return updated_service
        else:
            return None
    except Exception as e:
        logger.error(f"Error topping up balance for service {service_id}: {e}")
        raise


def get_services_by_category_id(category_id):
    try:
        services = service_repository.get_services_by_category_id(category_id)
        logger.info(f"Retrieved {len(services)} services for category {category_id}.")
        return services
    except Exception as e:
        logger.error(f"Error retrieving services for category {category_id}: {e}")
        raise


def soft_delete_service(service_id):
    try:
        service = service_repository.soft_delete_service(service_id)
        if service:
            logger.info(f"Service {service_id} soft deleted.")
            return service
        else:
            return None
    except Exception as e:
        logger.error(f"Error soft deleting service {service_id}: {e}")
        raise